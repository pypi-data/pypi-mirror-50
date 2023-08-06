import numpy as np
from xml.etree.ElementTree import Element
from .shape import Shape
from ..shape_util import (
    triangulate_edge,
    triangulate_ellipse,
    center_radii_to_corners,
    rectangle_to_box,
    poly_to_mask,
)


class Ellipse(Shape):
    """Class for a single ellipse

    Parameters
    ----------
    data : (4, 2) array or (2, 2) array.
        Either a (2, 2) array specifying the center and radii of an axis
        aligned ellipse, or a (4, 2) array specifying the four corners of a
        boudning box that contains the ellipse. These need not be axis aligned.
    edge_width : float
        thickness of lines and edges.
    edge_color : str | tuple
        If string can be any color name recognized by vispy or hex value if
        starting with `#`. If array-like must be 1-dimensional array with 3 or
        4 elements.
    face_color : str | tuple
        If string can be any color name recognized by vispy or hex value if
        starting with `#`. If array-like must be 1-dimensional array with 3 or
        4 elements.
    opacity : float
        Opacity of the shape, must be between 0 and 1.
    z_index : int
        Specifier of z order priority. Shapes with higher z order are displayed
        ontop of others.
    """

    def __init__(
        self,
        data,
        *,
        edge_width=1,
        edge_color='black',
        face_color='white',
        opacity=1,
        z_index=0,
    ):

        super().__init__(
            edge_width=edge_width,
            edge_color=edge_color,
            face_color=face_color,
            opacity=opacity,
            z_index=z_index,
        )

        self._closed = True
        self.data = np.array(data)
        self.name = 'ellipse'

    @property
    def data(self):
        """(4, 2) array: ellipse vertices.
        """
        return self._data

    @data.setter
    def data(self, data):
        if len(data) == 2:
            data = center_radii_to_corners(data[0], data[1])
        if len(data) != 4:
            raise ValueError(
                """Data shape does not match an ellipse.
                             Ellipse expects four corner vertices"""
            )
        else:
            # Build boundary vertices with num_segments
            vertices, triangles = triangulate_ellipse(data)
            self._set_meshes(vertices[1:-1], face=False)
            self._face_vertices = vertices
            self._face_triangles = triangles
            self._box = rectangle_to_box(data)
        self._data = data

    def transform(self, transform):
        """Performs a linear transform on the shape

        Parameters
        ----------
        transform : np.ndarray
            2x2 array specifying linear transform.
        """
        self._box = self._box @ transform.T
        self._data = self._data @ transform.T
        self._face_vertices = self._face_vertices @ transform.T

        points = self._face_vertices[1:-1]

        centers, offsets, triangles = triangulate_edge(
            points, closed=self._closed
        )
        self._edge_vertices = centers
        self._edge_offsets = offsets
        self._edge_triangles = triangles

    def to_mask(self, mask_shape=None, zoom_factor=1, offset=[0, 0]):
        """Convert the shape vertices to a boolean mask. 

        Set points lying inside the shape as `True`. Negative points or points
        outside the mask_shape after the zoom and offset are clipped.

        Parameters
        ----------
        mask_shape : np.ndarray | tuple | None
            1x2 array of shape of mask to be generated. If non specified, takes
            the max of the vertices.
        zoom_factor : float
            Premultiplier applied to coordinates before generating mask. Used
            for generating as downsampled mask.
        offset : 2-tuple
            Offset subtracted from coordinates before multiplying by the
            zoom_factor. Used for putting negative coordinates into the mask.

        Returns
        ----------
        mask : np.ndarray
            Boolean array with `True` for points inside the shape
        """
        if mask_shape is None:
            mask_shape = self.data.max(axis=0).astype('int')

        mask = poly_to_mask(
            mask_shape, (self._face_vertices - offset) * zoom_factor
        )

        return mask

    def to_xml(self):
        """Generates an xml element that defintes the shape according to the
        svg specification.

        Returns
        ----------
        element : xml.etree.ElementTree.Element
            xml element specifying the shape according to svg.
        """
        props = self.svg_props
        data = self.data[:, ::-1]

        offset = data[1] - data[0]
        angle = -np.arctan2(offset[0], -offset[1])
        if not angle == 0:
            # if shape has been rotated, shift to origin
            cen = data.mean(axis=0)
            coords = data - cen

            # rotate back to axis aligned
            c, s = np.cos(angle), np.sin(-angle)
            rotation = np.array([[c, s], [-s, c]])
            coords = coords @ rotation.T

            # shift back to center
            coords = coords + cen

            # define rotation around center
            transform = f'rotate({np.degrees(-angle)} {cen[0]} {cen[1]})'
            props['transform'] = transform
        else:
            coords = data

        cx = str(cen[0])
        cy = str(cen[1])
        size = abs(coords[2] - coords[0])
        rx = str(size[0] / 2)
        ry = str(size[1] / 2)

        element = Element('ellipse', cx=cx, cy=cy, rx=rx, ry=ry, **props)
        return element
