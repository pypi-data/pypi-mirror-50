import numpy as np
from os.path import join
from astropy.coordinates import CartesianRepresentation,\
    CartesianDifferential, ICRS
from astropy.coordinates.matrix_utilities import rotation_matrix
import astropy.units as U
import astropy.constants as C
from ._L_align import L_align
from ._cartesian_translation import translate, translate_d

# Extend CartesianRepresentation to allow coordinate translation
setattr(CartesianRepresentation, 'translate', translate)

# Extend CartesianDifferential to allow velocity (or other differential)
# translation
setattr(CartesianDifferential, 'translate', translate_d)


class SPHSource(object):
    """
    Class abstracting HI emission sources consisting of SPH simulation
    particles.

    This class constructs an HI emission source from arrays of SPH particle
    properties: mass, smoothing length, temperature, position, and velocity.

    Parameters
    ----------
    distance : astropy.units.Quantity, with dimensions of length
        Source distance, also used to set the velocity offset via Hubble's law.

    vpeculiar : astropy.units.Quantity, with dimensions of velocity
        Source peculiar velocity, added to the velocity from Hubble's law.

    rotation : dict
        Keys may be any combination of 'axis_angle', 'rotmat' and/or
        'L_coords'. These will be applied in this order. Note that the 'y-z'
        plane will be the one eventually placed in the plane of the "sky". The
        corresponding values:
        - 'axis_angle' : 2-tuple, first element one of 'x', 'y', 'z' for the \
        axis to rotate about, second element an astropy.units.Quantity with \
        dimensions of angle, indicating the angle to rotate through.
        - 'rotmat' : A (3, 3) numpy.array specifying a rotation.
        - 'L_coords' : A 2-tuple containing an inclination and an azimuthal \
        angle (both astropy.units.Quantity instances with dimensions of \
        angle). The routine will first attempt to identify a preferred plane \
        based on the angular momenta of the central 1/3 of particles in the \
        source. This plane will then be rotated to lie in the plane of the \
        "sky" ('y-z'), rotated by the azimuthal angle about its angular \
        momentum pole (rotation about 'x'), and inclined (rotation about 'y').

    ra : astropy.units.Quantity, with dimensions of angle
        Right ascension for the source centroid.

    dec : astropy.units.Quantity, with dimensions of angle
        Declination for the source centroid.

    h : float
        Dimensionless hubble constant, H0 = h * 100 km / s / Mpc.

    T_g : astropy.units.Quatity, with dimensions of temperature
        Particle temperature.

    mHI_g : astropy.unit.Quantity, with dimensions of mass
        Particle HI mass.

    xyz_g : astropy.units.Quantity array of length 3, with dimensions of length
        Particle position offset from source centroid. Note that the 'y-z'
        plane is that eventually placed in the plane of the "sky"; 'x' is
        the axis corresponding to the "line of sight".

    vxyz_g : astropy.units.Quantity array of length 3, with dimensions of \
    velocity
        Particle velocity offset from source centroid. Note that the 'y-z'
        plane is that eventually placed in the plane of the "sky"; 'x' is
        the axis corresponding to the "line of sight".

    hsm_g : astropy.units.Quantity, with dimensions of length
        Particle SPH smoothing lengths.

    Returns
    -------
    out : SPHSource
        An appropriately initialized SPHSource object.

    See Also
    --------
    SingleParticleSource (simplest possible implementation of a class \
    inheriting from SPHSource).
    CrossSource
    SOSource
    """

    def __init__(
            self,
            distance=3. * U.Mpc,
            vpeculiar=0. * U.km / U.s,
            rotation={'rotmat': np.eye(3)},
            ra=0.*U.deg,
            dec=0.*U.deg,
            h=.7,
            T_g=None,
            mHI_g=None,
            xyz_g=None,
            vxyz_g=None,
            hsm_g=None,
            coordinate_axis=None
    ):

        if coordinate_axis is None:
            if (xyz_g.shape[0] == 3) and (xyz_g.shape[1] != 3):
                coordinate_axis = 0
            elif (xyz_g.shape[0] != 3) and (xyz_g.shape[1] == 3):
                coordinate_axis = 1
            elif xyz_g.shape == (3, 3):
                raise RuntimeError("martini.sources.SPHSource: cannot guess "
                                   "coordinate_axis with shape (3, 3), provide"
                                   " explicitly.")
            else:
                raise RuntimeError("martini.sources.SPHSource: incorrect "
                                   "coordinate shape (not (3, N) or (N, 3)).")

        if xyz_g.shape != vxyz_g.shape:
            raise ValueError("martini.sources.SPHSource: xyz_g and vxyz_g must"
                             " have matching shapes.")
        self.h = h
        self.T_g = T_g
        self.mHI_g = mHI_g
        self.coordinates_g = CartesianRepresentation(
            xyz_g,
            xyz_axis=coordinate_axis,
            differentials={'s': CartesianDifferential(
                vxyz_g,
                xyz_axis=coordinate_axis
            )}
        )
        self.hsm_g = hsm_g

        self.npart = self.mHI_g.size

        self.ra = ra
        self.dec = dec
        self.distance = distance
        self.vpeculiar = vpeculiar
        self.rotation = rotation
        self.current_rotation = np.eye(3)
        self.rotate(**self.rotation)
        self.rotate(axis_angle=('y', self.dec))
        self.rotate(axis_angle=('z', -self.ra))
        direction_vector = np.array([
            np.cos(self.ra) * np.cos(self.dec),
            np.sin(self.ra) * np.cos(self.dec),
            np.sin(self.dec)
        ])
        distance_vector = direction_vector * self.distance
        self.translate_position(distance_vector)
        self.vsys = \
            (self.h * 100.0 * U.km * U.s ** -1 * U.Mpc ** - 1) * self.distance
        hubble_flow_vector = direction_vector * self.vsys
        vpeculiar_vector = direction_vector * self.vpeculiar
        self.translate_velocity(hubble_flow_vector + vpeculiar_vector)
        self.sky_coordinates = ICRS(self.coordinates_g)
        return

    def apply_mask(self, mask):
        """
        Remove particles from source arrays according to a mask.

        Parameters
        ----------
        mask : array-like, containing boolean-like
            Remove particles with indices corresponding to False values from
            the source arrays.
        """

        self.T_g = self.T_g[mask]
        self.mHI_g = self.mHI_g[mask]
        self.coordinates_g = self.coordinates_g[mask]
        self.sky_coordinates = ICRS(self.coordinates_g)
        self.hsm_g = self.hsm_g[mask]
        self.npart = np.sum(mask)
        if self.npart == 0:
            raise RuntimeError('No source particles in target region.')
        return

    def rotate(self, axis_angle=None, rotmat=None, L_coords=None):
        """
        Rotate the source.

        The arguments correspond to different rotation types. If supplied
        together in one function call, they are applied in order: axis_angle,
        then rotmat, then L_coords.

        Parameters
        ----------
        axis_angle : 2-tuple
            First element one of 'x', 'y', 'z' for the axis to rotate about,
            second element an astropy.units.Quantity with dimensions of angle,
            indicating the angle to rotate through.
        rotmat : (3, 3) array-like
            Rotation matrix.
        L_coords : 2-tuple
            First element containing an inclination and second element an
            azimuthal angle (both astropy.units.Quantity instances with
            dimensions of angle). The routine will first attempt to identify
            a preferred plane based on the angular momenta of the central 1/3
            of particles in the source. This plane will then be rotated to lie
            in the 'y-z' plane, followed by a rotation by the azimuthal angle
            about its angular momentum pole (rotation about 'x'), and finally
            inclined (rotation about 'y').
        """

        do_rot = np.eye(3)

        if axis_angle is not None:
            do_rot = rotation_matrix(
                axis_angle[1],
                axis=axis_angle[0]
            ).dot(do_rot)

        if rotmat is not None:
            do_rot = rotmat.dot(do_rot)

        if L_coords is not None:
            incl, az_rot = L_coords
            do_rot = L_align(self.coordinates_g.get_xyz(),
                             self.coordinates_g.differentials['s'].get_d_xyz(),
                             self.mHI_g, frac=.3, Laxis='x').dot(do_rot)
            do_rot = rotation_matrix(az_rot, axis='x').dot(do_rot)
            do_rot = rotation_matrix(incl, axis='y').dot(do_rot)

        self.current_rotation = do_rot.dot(self.current_rotation)
        self.coordinates_g = self.coordinates_g.transform(do_rot)
        return

    def translate_position(self, translation_vector):
        """
        Translate the source.

        Note that the "line of sight" is along the 'x' axis.

        Parameters
        ----------
        translation_vector : astropy.units.Quantity, shape (3, ), with \
        dimensions of length
            Vector by which to offset the source particle coordinates.
        """

        self.coordinates_g = self.coordinates_g.translate(translation_vector)
        return

    def translate_velocity(self, translation_vector):
        """
        Apply an offset to the source velocity.

        Note that the "line of sight" is along the 'x' axis.

        Parameters
        ----------
        translation_vector : astropy.units.Quantity, shape (3, ), with \
        dimensions of velocity
            Vector by which to offset the source particle velocities.
        """

        self.coordinates_g.differentials['s'] = \
            self.coordinates_g.differentials['s'].translate(translation_vector)
        return

    def save_current_rotation(self, fname):
        """
        Output current rotation matrix to file.

        Parameters
        ----------
        fname : filename or file handle
            File in which to save rotation matrix.
        """

        np.savetxt(fname, self.current_rotation)
        return


class SingleParticleSource(SPHSource):
    """
    Class illustrating inheritance from martini.sources.SPHSource, creates a
    single particle test source.

    A simple test source consisting of a single particle will be created. The
    particle has a mass of 10^4 Msun, a SPH smoothing length of 1 kpc, a
    temperature of 10^4 K, a position offset by (x, y, z) = (1 pc, 1 pc, 1 pc)
    from the source centroid, a peculiar velocity of 0 km/s, and will be placed
    in the Hubble flow assuming h = 0.7 and the distance provided.

    Parameters
    ----------
    distance : astropy.units.Quantity, with units of length
        Source distance, also used to place the source in the Hubble flow
        assuming h = 0.7.

    vpeculiar : astropy.units.Quantity, with dimensions of velocity
        Source peculiar velocity, added to the velocity from Hubble's law.

    ra : astropy.units.Quantity, with dimensions of angle
        Right ascension for the source centroid.

    dec : astropy.units.Quantity, with dimensions of angle
        Declination for the source centroid.

    Returns
    -------
    out : SingleParticleSource
        An appropriately initialized SingleParticleSource object.
    """

    def __init__(
            self,
            distance=3 * U.Mpc,
            vpeculiar=0 * U.km / U.s,
            ra=0. * U.deg,
            dec=0. * U.deg
    ):

        super().__init__(
            distance=distance,
            vpeculiar=vpeculiar,
            rotation={'rotmat': np.eye(3)},
            ra=ra,
            dec=dec,
            h=.7,
            T_g=np.ones(1) * 1.E4 * U.K,
            mHI_g=np.ones(1) * 1.E4 * U.solMass,
            xyz_g=np.ones((1, 3)) * 1.E-3 * U.kpc,
            vxyz_g=np.zeros((1, 3)) * U.km * U.s ** -1,
            hsm_g=np.ones(1) * U.kpc
            )
        return


class CrossSource(SPHSource):
    """
    Creates a source consisting of 4 particles arrayed in an asymmetric cross.

    A simple test source consisting of four particles will be created. Each has
    a mass of 10^4 Msun, a SPH smoothing length of 1 kpc, a temperature of
    10^4 K, and will be placed in the Hubble flow assuming h=.7 and a distance
    of 3 Mpc. Particle coordinates in kpc are
    [[0,  1,  0],
    [0,  0,  2],
    [0, -3,  0],
    [0,  0, -4]]
    and velocities in km/s are
    [[0,  0,  1],
    [0, -1,  0],
    [0,  0, -1],
    [0,  1,  0]]

    Parameters
    ----------
    distance : astropy.units.Quantity, with units of length
        Source distance, also used to place the source in the Hubble flow
        assuming h = 0.7.

    vpeculiar : astropy.units.Quantity, with dimensions of velocity
        Source peculiar velocity, added to the velocity from Hubble's law.

    rotation : dict
        Keys may be any combination of 'axis_angle', 'rotmat' and/or
        'L_coords'. These will be applied in this order. Note that the 'y-z'
        plane will be the one eventually placed in the plane of the "sky". The
        corresponding values:
        - 'axis_angle' : 2-tuple, first element one of 'x', 'y', 'z' for the \
        axis to rotate about, second element an astropy.units.Quantity with \
        dimensions of angle, indicating the angle to rotate through.
        - 'rotmat' : A (3, 3) numpy.array specifying a rotation.
        - 'L_coords' : A 2-tuple containing an inclination and an azimuthal \
        angle (both astropy.units.Quantity instances with dimensions of \
        angle). The routine will first attempt to identify a preferred \
        plane based on the angular momenta of the central 1/3 of particles \
        in the source. This plane will then be rotated to lie in the plane \
        of the "sky" ('y-z'), rotated by the azimuthal angle about its \
        angular momentum pole (rotation about 'x'), and inclined (rotation \
        about 'y').

    ra : astropy.units.Quantity, with dimensions of angle
        Right ascension for the source centroid.

    dec : astropy.units.Quantity, with dimensions of angle
        Declination for the source centroid.

    Returns
    -------
    out : CrossSource
        An appropriately initialized CrossSource object.
    """

    def __init__(
            self,
            distance=3. * U.Mpc,
            vpeculiar=0 * U.km / U.s,
            rotation={'rotmat': np.eye(3)},
            ra=0. * U.deg,
            dec=0. * U.deg
    ):

        xyz_g = np.array([[0, 1, 0],
                          [0, 0, 2],
                          [0, -3, 0],
                          [0, 0, -4]]) * U.kpc,

        vxyz_g = np.array([[0, 0, 1],
                           [0, -1, 0],
                           [0, 0, -1],
                           [0, 1, 0]]) * U.km * U.s ** -1

        super().__init__(
            distance=distance,
            vpeculiar=vpeculiar,
            rotation={'rotmat': np.eye(3)},
            ra=ra,
            dec=dec,
            h=.7,
            T_g=np.ones(4) * 1.E4 * U.K,
            mHI_g=np.ones(4) * 1.E4 * U.solMass,
            xyz_g=xyz_g,
            vxyz_g=vxyz_g,
            hsm_g=np.ones(4) * U.kpc
        )
        return


class SOSource(SPHSource):
    """
    Class abstracting HI sources using the SimObj package for interface to
    simulation data.

    This class accesses simulation data via the SimObj package
    (https://github.com/kyleaoman/simobj); see the documentation of that
    package for further configuration instructions.

    Parameters
    ----------
    distance : astropy.units.Quantity, with dimensions of length
        Source distance, also used to set the velocity offset via Hubble's law.

    vpeculiar : astropy.units.Quantity, with dimensions of velocity
        Source peculiar velocity, added to the velocity from Hubble's law.

    rotation : dict
        Keys may be any combination of 'axis_angle', 'rotmat' and/or
        'L_coords'. These will be applied in this order. Note that the 'y-z'
        plane will be the one eventually placed in the plane of the "sky". The
        corresponding values:
        - 'axis_angle' : 2-tuple, first element one of 'x', 'y', 'z' for the \
        axis to rotate about, second element an astropy.units.Quantity with \
        dimensions of angle, indicating the angle to rotate through.
        - 'rotmat' : A (3, 3) numpy.array specifying a rotation.
        - 'L_coords' : A 2-tuple containing an inclination and an azimuthal \
        angle (both astropy.units.Quantity instances with dimensions of \
        angle). The routine will first attempt to identify a preferred plane \
        based on the angular momenta of the central 1/3 of particles in the \
        source. This plane will then be rotated to lie in the plane of the \
        "sky" ('y-z'), rotated by the azimuthal angle about its angular \
        momentum pole (rotation about 'x'), and inclined (rotation about 'y').

    ra : astropy.units.Quantity, with dimensions of angle
        Right ascension for the source centroid.

    dec : astropy.units.Quantity, with dimensions of angle
        Declination for the source centroid.

    SO_args : dict
        Dictionary of keyword arguments to pass to a call to simobj.SimObj.
        Arguments are: 'obj_id', 'snap_id', 'mask_type', 'mask_args',
        'mask_kwargs', 'configfile', 'simfiles_configfile', 'ncpu'. See simobj
        package documentation for details. Provide SO_args or SO_instance, not
        both.

    SO_instance : SimObj instance
        An initialized SimObj object. Provide SO_instance or SO_args, not both.

    Returns
    -------
    out : SOSource
        An appropriately initialized SOSource object.
    """

    def __init__(
            self,
            distance=3.*U.Mpc,
            vpeculiar=0*U.km/U.s,
            rotation={'L_coords': (60.*U.deg, 0.*U.deg)},
            ra=0.*U.deg,
            dec=0.*U.deg,
            SO_args=None,
            SO_instance=None
    ):

        from simobj import SimObj  # optional dependency for this source class

        self._SO_args = SO_args
        if (SO_args is not None) and (SO_instance is not None):
            raise ValueError('martini.source.SOSource: Provide SO_args or '
                             'SO_instance, not both.')
        if SO_args is not None:
            with SimObj(**self._SO_args) as SO:
                super().__init__(
                    distance=distance,
                    rotation=rotation,
                    ra=ra,
                    dec=dec,
                    h=SO.h,
                    T_g=SO.T_g,
                    mHI_g=SO.mHI_g,
                    xyz_g=SO.xyz_g,
                    vxyz_g=SO.vxyz_g,
                    hsm_g=SO.hsm_g
                )
        elif SO_instance is not None:
            super().__init__(
                distance=distance,
                vpeculiar=vpeculiar,
                rotation=rotation,
                ra=ra,
                dec=dec,
                h=SO_instance.h,
                T_g=SO_instance.T_g,
                mHI_g=SO_instance.mHI_g,
                xyz_g=SO_instance.xyz_g,
                vxyz_g=SO_instance.vxyz_g,
                hsm_g=SO_instance.hsm_g
            )
        else:
            raise ValueError('martini.sources.SOSource: Provide one of SO_args'
                             ' or SO_instance.')
        return


class TNGSource(SPHSource):
    """
    Class abstracting HI sources designed to run in the IllustrisTNG JupyterLab
    environment for access to simulation data. Can also be used in other
    environments, but requires that the 'illustris_python' module be
    importable, and further that the data are laid out on disk in the fiducial
    way (see: http://www.tng-project.org/data/docs/scripts/).

    Parameters
    ----------
    basePath : string
        Directory containing simulation data, for instance 'TNG100-1/output/',
        see also http://www.tng-project.org/data/docs/scripts/

    snapNum : int
        Snapshot number. In TNG, snapshot 99 is the final output. Note that
        a full snapshot (not a 'mini' snapshot, see
        http://www.tng-project.org/data/docs/specifications/#sec1a) must be
        used.

    subID : int
        Subhalo ID of the target object. Note that all particles in the FOF
        group to which the subhalo belongs are used to construct the data cube.
        This avoids strange "holes" at the locations of other subhaloes in the
        same group, and gives a more realistic treatment of foreground and
        background emission local to the source.

    distance : astropy.units.Quantity, with dimensions of length
        Source distance, also used to set the velocity offset via Hubble's law.

    vpeculiar : astropy.units.Quantity, with dimensions of velocity
        Source peculiar velocity, added to the velocity from Hubble's law.

    rotation : dict
        Keys may be any combination of 'axis_angle', 'rotmat' and/or
        'L_coords'. These will be applied in this order. Note that the 'y-z'
        plane will be the one eventually placed in the plane of the "sky". The
        corresponding values:
        - 'axis_angle' : 2-tuple, first element one of 'x', 'y', 'z' for the \
        axis to rotate about, second element an astropy.units.Quantity with \
        dimensions of angle, indicating the angle to rotate through.
        - 'rotmat' : A (3, 3) numpy.array specifying a rotation.
        - 'L_coords' : A 2-tuple containing an inclination and an azimuthal \
        angle (both astropy.units.Quantity instances with dimensions of \
        angle). The routine will first attempt to identify a preferred plane \
        based on the angular momenta of the central 1/3 of particles in the \
        source. This plane will then be rotated to lie in the plane of the \
        "sky" ('y-z'), rotated by the azimuthal angle about its angular \
        momentum pole (rotation about 'x'), and inclined (rotation about 'y').

    ra : astropy.units.Quantity, with dimensions of angle
        Right ascension for the source centroid.

    dec : astropy.units.Quantity, with dimensions of angle
        Declination for the source centroid.

    Returns
    -------
    out : TNGSource
        An appropriately initialized TNGSource object.
    """

    def __init__(
            self,
            basePath,
            snapNum,
            subID,
            distance=3.*U.Mpc,
            vpeculiar=0*U.km/U.s,
            rotation={'L_coords': (60.*U.deg, 0.*U.deg)},
            ra=0.*U.deg,
            dec=0.*U.deg
    ):

        # optional dependencies for this source class
        from illustris_python.groupcat import loadSingle, loadHeader
        from illustris_python.snapshot import loadSubset, getSnapOffsets
        from Hdecompose.atomic_frac import atomic_frac

        X_H = 0.76
        data_header = loadHeader(basePath, snapNum)
        data_sub = loadSingle(basePath, snapNum, subhaloID=subID)
        haloID = data_sub['SubhaloGrNr']
        fields_g = ('Masses', 'Velocities', 'InternalEnergy',
                    'ElectronAbundance', 'Density')
        subset_g = getSnapOffsets(basePath, snapNum, haloID, "Group")
        data_g = loadSubset(basePath, snapNum, 'gas', fields=fields_g,
                            subset=subset_g)
        try:
            data_g.update(loadSubset(basePath, snapNum, 'gas',
                                     fields=('CenterOfMass', ),
                                     subset=subset_g, sq=False))
        except Exception as exc:
            if ('Particle type' in exc.args[0]) and \
               ('does not have field' in exc.args[0]):
                data_g.update(loadSubset(basePath, snapNum, 'gas',
                                         fields=('Coordinates', ),
                                         subset=subset_g, sq=False))
            else:
                raise
        try:
            data_g.update(loadSubset(basePath, snapNum, 'gas',
                                     fields=('GFM_Metals', ), subset=subset_g,
                                     mdi=(0, ), sq=False))
        except Exception as exc:
            if ('Particle type' in exc.args[0]) and \
               ('does not have field' in exc.args[0]):
                X_H_g = X_H
            else:
                raise
        else:
            X_H_g = data_g['GFM_Metals']  # only loaded column 0: Hydrogen

        a = data_header['Time']
        z = data_header['Redshift']
        h = data_header['HubbleParam']
        xe_g = data_g['ElectronAbundance']
        rho_g = data_g['Density'] * 1E10 / h * U.Msun \
            * np.power(a / h * U.kpc, -3)
        u_g = data_g['InternalEnergy']  # unit conversion handled in T_g
        mu_g = 4 * C.m_p.to(U.g).value / (1 + 3 * X_H_g + 4 * X_H_g * xe_g)
        gamma = 5. / 3.  # see http://www.tng-project.org/data/docs/faq/#gen4
        T_g = (gamma - 1) * u_g / C.k_B.to(U.erg / U.K).value * 1E10 * mu_g \
            * U.K
        m_g = data_g['Masses'] * 1E10 / h * U.Msun
        # cast to float64 to avoid underflow error
        nH_g = U.Quantity(rho_g * X_H_g / mu_g, dtype=np.float64) / C.m_p
        # In TNG_corrections I set f_neutral = 1 for particles with density
        # > .1cm^-3. Might be possible to do a bit better here, but HI & H2
        # tables for TNG will be available soon anyway.
        fatomic_g = atomic_frac(
            z,
            nH_g,
            T_g,
            rho_g,
            X_H_g,
            onlyA1=True,
            TNG_corrections=True
        )
        mHI_g = m_g * X_H_g * fatomic_g
        try:
            xyz_g = data_g['CenterOfMass'] * a / h * U.kpc
        except KeyError:
            xyz_g = data_g['Coordinates'] * a / h * U.kpc
        vxyz_g = data_g['Velocities'] * np.sqrt(a) * U.km / U.s
        V_cell = data_g['Masses'] / data_g['Density'] \
            * np.power(a / h * U.kpc, 3)  # Voronoi cell volume
        r_cell = np.power(3. * V_cell / 4. / np.pi, 1. / 3.).to(U.kpc)
        hsm_g = 2.5 * r_cell  # in mind a cubic spline that =0 at h, I think
        xyz_centre = data_sub['SubhaloPos'] * a / h * U.kpc
        xyz_g -= xyz_centre
        vxyz_centre = data_sub['SubhaloVel'] * np.sqrt(a) * U.km / U.s
        vxyz_g -= vxyz_centre

        super().__init__(
            distance=distance,
            vpeculiar=vpeculiar,
            rotation=rotation,
            ra=ra,
            dec=dec,
            h=h,
            T_g=T_g,
            mHI_g=mHI_g,
            xyz_g=xyz_g,
            vxyz_g=vxyz_g,
            hsm_g=hsm_g
        )
        return


class EAGLESource(SPHSource):
    """
    Class abstracting HI sources designed to work with publicly available
    EAGLE snapshot + group files. For file access, see
    http://icc.dur.ac.uk/Eagle/database.php.

    Parameters
    ----------
    snapPath : string
        Directory containing snapshot files.

    snapBase : string
        Filename of snapshot files, omitting portion '.X.hdf5'. Note these must
        be the subfind-processed files, usually named 
        'eagle_subfind_particles[...]'.

    groupPath : string
        Directory containing group catalog files.

    groupBase : string
        Filename of group catalog files, omitting portion '.X.hdf5'. Note
        these must be the subfind tables, usually named 
        'eagle_subfind_tab[...]'.

    fof : int
        FOF group number of the target object. Note that all particles in the
        FOF group to which the subhalo belongs are used to construct the data
        cube. This avoids strange "holes" at the locations of other subhaloes
        in the same group, and gives a more realistic treatment of foreground
        and background emission local to the source. In the EAGLE database,
        this is the 'GroupNumber'.

    sub : int
        Subfind subhalo number of the target object. For centrals the subhalo
        number is 0, for satellites >0. In the EAGLE database, this is then
        'SubGroupNumber'.

    subBoxSize : astropy.units.Quantity, with dimensions of length
        Box half-side length of a region to load around the object of interest,
        in physical (not comoving, no little h) units. This is only to avoid
        needing to load the entire particle arrays. By default set to 1 Mpc,
        which should be adequate for most galaxies.

    distance : astropy.units.Quantity, with dimensions of length
        Source distance, also used to set the velocity offset via Hubble's law.

    vpeculiar : astropy.units.Quantity, with dimensions of velocity
        Source peculiar velocity, added to the velocity from Hubble's law.

    rotation : dict
        Keys may be any combination of 'axis_angle', 'rotmat' and/or
        'L_coords'. These will be applied in this order. Note that the 'y-z'
        plane will be the one eventually placed in the plane of the "sky". The
        corresponding values:
        - 'axis_angle' : 2-tuple, first element one of 'x', 'y', 'z' for the \
        axis to rotate about, second element an astropy.units.Quantity with \
        dimensions of angle, indicating the angle to rotate through.
        - 'rotmat' : A (3, 3) numpy.array specifying a rotation.
        - 'L_coords' : A 2-tuple containing an inclination and an azimuthal \
        angle (both astropy.units.Quantity instances with dimensions of \
        angle). The routine will first attempt to identify a preferred plane \
        based on the angular momenta of the central 1/3 of particles in the \
        source. This plane will then be rotated to lie in the plane of the \
        "sky" ('y-z'), rotated by the azimuthal angle about its angular \
        momentum pole (rotation about 'x'), and inclined (rotation about 'y').

    ra : astropy.units.Quantity, with dimensions of angle
        Right ascension for the source centroid.

    dec : astropy.units.Quantity, with dimensions of angle
        Declination for the source centroid.

    Returns
    -------
    out : EAGLESource
        An appropriately initialized EAGLESource object.
    """

    def __init__(
            self,
            snapPath=None,
            snapBase=None,
            groupPath=None,
            groupBase=None,
            fof=None,
            sub=None,
            subBoxSize=1*U.Mpc,
            distance=3.*U.Mpc,
            vpeculiar=0*U.km/U.s,
            rotation={'L_coords': (60.*U.deg, 0.*U.deg)},
            ra=0.*U.deg,
            dec=0.*U.deg
    ):

        if snapPath is None:
            raise ValueError('Provide snapPath argument to EAGLESource.')
        if snapBase is None:
            raise ValueError('Provide snapBase argument to EAGLESource.')
        if groupPath is None:
            raise ValueError('Provide groupPath argument to EAGLESource.')
        if groupBase is None:
            raise ValueError('Provide groupBase argument to EAGLESource.')
        if fof is None:
            raise ValueError('Provide fof argument to EAGLESource.')
        if sub is None:
            raise ValueError('Provide sub argument to EAGLESource.')

        # optional dependencies for this source class
        from read_eagle import EagleSnapshot
        from Hdecompose.atomic_frac import atomic_frac
        import h5py

        fileN = 0
        while True:  # will break when group found or raise when out of files
            groupFile = join(groupPath, groupBase+'.{:d}.hdf5'.format(fileN))
            with h5py.File(groupFile, 'r') as g:
                mask = np.logical_and(
                    np.array(g['/Subhalo/GroupNumber']) == fof,
                    np.array(g['/Subhalo/SubGroupNumber']) == sub
                )
                if not np.sum(mask):
                    fileN += 1
                    continue  # group not in this file, try next one
                a = g['Header'].attrs['Time']
                redshift = 1 / a - 1
                h = g['Header'].attrs['HubbleParam']
                lbox = g['Header'].attrs['BoxSize'] * U.Mpc / h
                code_to_g = g['/Units'].attrs['UnitMass_in_g'] * U.g
                code_to_cm = g['/Units'].attrs['UnitLength_in_cm'] * U.cm
                code_to_cm_s = g['/Units'].attrs['UnitVelocity_in_cm_per_s'] \
                    * U.cm / U.s
                dset = g['/Subhalo/CentreOfPotential']
                aexp = dset.attrs.get('aexp-scale-exponent')
                hexp = dset.attrs.get('h-scale-exponent')
                cop = (dset[mask, :] * np.power(a, aexp) * np.power(h, hexp)
                       * code_to_cm).to(U.kpc)
                dset = g['/Subhalo/Velocity']
                aexp = dset.attrs.get('aexp-scale-exponent')
                hexp = dset.attrs.get('h-scale-exponent')
                vcent = (dset[mask, :] * np.power(a, aexp) * np.power(h, hexp)
                         * code_to_cm_s).to(U.km / U.s)
                break

        snapFile = join(snapPath, snapBase+'.0.hdf5')
        subBoxSize = (subBoxSize * h / a).to(U.Mpc).value
        centre = (cop * h / a).to(U.Mpc).value
        eagle_data = EagleSnapshot(snapFile)
        region = np.vstack((
            centre - subBoxSize,
            centre + subBoxSize
        )).T.flatten()
        eagle_data.select_region(*region)

        with h5py.File(snapFile, 'r') as f:

            fH = f['/RuntimePars'].attrs['InitAbundance_Hydrogen']
            fHe = f['/RuntimePars'].attrs['InitAbundance_Helium']
            proton_mass = f['/Constants'].attrs['PROTONMASS'] * U.g
            mu = 1 / (fH + .25 * fHe)
            gamma = f['/RuntimePars'].attrs['EOS_Jeans_GammaEffective']
            T0 = f['/RuntimePars'].attrs['EOS_Jeans_TempNorm_K'] * U.K

            def fetch(att, ptype=0):
                # gas is type 0, only need gas properties
                tmp = eagle_data.read_dataset(ptype, att)
                dset = f['/PartType{:d}/{:s}'.format(ptype, att)]
                aexp = dset.attrs.get('aexp-scale-exponent')
                hexp = dset.attrs.get('h-scale-exponent')
                return np.array(tmp, dtype='f8') * np.power(a, aexp) \
                    * np.power(h, hexp)

            ng_g = fetch('GroupNumber')
            particles = dict(
                xyz_g=(fetch('Coordinates') * code_to_cm).to(U.kpc),
                vxyz_g=(fetch('Velocity') * code_to_cm_s).to(U.km / U.s),
                T_g=fetch('Temperature') * U.K,
                hsm_g=(fetch('SmoothingLength') * code_to_cm).to(U.kpc)
            )
            rho_g = fetch('Density') * U.g * U.cm ** -3
            SFR_g = fetch('StarFormationRate')
            Habundance_g = fetch('ElementAbundance/Hydrogen')

        particles['mHI_g'] = (atomic_frac(
            redshift,
            rho_g * Habundance_g / (mu * proton_mass),
            particles['T_g'],
            rho_g,
            Habundance_g,
            onlyA1=True,
            EAGLE_corrections=True,
            SFR=SFR_g,
            mu=mu,
            gamma=gamma,
            fH=fH,
            T0=T0
        ) * code_to_g).to(U.solMass)

        mask = ng_g == fof
        for k, v in particles.items():
            particles[k] = v[mask]

        particles['xyz_g'] -= cop
        particles['xyz_g'][particles['xyz_g'] > lbox / 2.] -= lbox.to(U.kpc)
        particles['xyz_g'][particles['xyz_g'] < -lbox / 2.] += lbox.to(U.kpc)
        particles['vxyz_g'] -= vcent

        super().__init__(
            distance=distance,
            vpeculiar=vpeculiar,
            rotation=rotation,
            ra=ra,
            dec=dec,
            h=h,
            **particles
        )
        return
