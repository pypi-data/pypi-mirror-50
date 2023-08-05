class TransformRef:
    """
    Reference to a Unity transform with a given transform path, along with an optional sibling index that can be used
    to distinguish between sibling transforms with the same path. Also contains optional references to parent and child
    transforms to allow navigation of the transform hierarchy.

    If the ``children`` attribute is None, it simply means that the attribute is uninitialized. The referenced
    transform may or may not actually have children.

    If the ``children`` attribute is an empty list, it means the referenced transform has no children.
    """

    def __init__(self, transform_path, sibling_index=-1, parent=None):
        """
        Initializes this TransformRef instance.

        :param transform_path: Parent-relative transform path, or the absolute path if ``parent`` is None.
        :param sibling_index: Optional sibling index, used to distinguish between sibling transforms with the same path.
        :param parent: Optional parent transform reference.
        """
        # Make sure the transform path is valid.
        if not isinstance(transform_path, str):
            raise ValueError("transform_path must be of type str")

        # Make sure the parent transform reference is valid.
        if (parent is not None) and not isinstance(parent, TransformRef):
            raise ValueError("parent must be None or of type TransformRef")

        # Define instance attributes.
        self.id = id
        self.transform_path = transform_path
        self.sibling_index = sibling_index
        self.children = None
        self.parent = None

        self.set_parent(parent)

    def set_parent(self, parent):
        """
        Set the parent transform reference.

        :param parent: Parent transform reference.
        :return: None.
        """
        # Make sure the parent transform reference is valid.
        if (parent is not None) and not isinstance(parent, TransformRef):
            raise ValueError("parent must be None or of type TransformRef")

        # Do nothing if the parent hasn't changed.
        if self.parent is parent:
            return

        # Unset the old parent.
        old_parent = self.parent
        if old_parent is not None:
            old_parent.remove_child(self)

        # Set the new parent.
        self.parent = parent
        if parent is not None:
            parent.add_child(self)

    def add_child(self, child):
        """
        Adds the child transform reference if it doesn't exist. Also converts the child's transform path to
        a parent-relative path.

        :param child: Child transform reference.
        :return: None.
        """
        # Make sure we have a valid transform reference.
        if not isinstance(child, TransformRef):
            raise ValueError("child must be of type TransformRef")

        # Make sure we have a valid list.
        if self.children is None:
            self.children = []

        # Add the child and update its transform path.
        #
        # Note that transform references with a parent use parent-relative transform paths.
        if child not in self.children:
            child.parent = self
            child.transform_path = child.get_relative_transform_path()
            self.children.append(child)

    def remove_child(self, child):
        """
        Removes the child transform reference if it exists. Also converts the child's transform path to
        an absolute path.

        :param child: Child transform reference.
        :return: None.
        """
        # Make sure we have a valid transform reference.
        if not isinstance(child, TransformRef):
            raise ValueError("child must be of type TransformRef")

        # Bail if we don't have a valid list.
        if self.children is None:
            return

        # Remove the child and update its transform path.
        #
        # Note that transform references without a parent use absolute transform paths.
        if child in self.children:
            child.transform_path = child.get_absolute_transform_path()
            child.parent = None
            self.children.remove(child)

    def get_relative_transform_path(self):
        """
        Gets the parent-relative path of the transform reference.

        :return: The parent-relative transform path, if the transform reference has a parent; otherwise, the absolute
        transform path.
        """
        path = self.transform_path

        if self.parent is not None:
            path = path.split('/')[-1]

        return path

    def get_absolute_transform_path(self):
        """
        Gets the absolute path of the transform reference by traversing its parents.

        :return: The absolute transform path.
        """
        path = self.transform_path

        parent = self.parent
        while parent is not None:
            path = "{0}/{1}".format(parent.transform_path, path)
            parent = parent.parent

        return path

    def _get_sibling_indices(self, absolute_transform_path):
        """
        Constructs a list containing the sibling indices of this transform reference and all its ancestors, which is
        used to distinguish between transforms with the same transform path.

        Ancestor sibling indices are listed before descendants.

        The number of sibling indices will match the number of sections in the transform path of this transform
        reference. For example, if the transform path is "PauseMenu/ReplayButton/Text", this method will return 3
        sibling indices. If there aren't enough sibling indices available, the list will be left-padded with `None`.

        If all sibling indices are -1, this method will return `None` instead of a list. This shorthand not only
        decreases the size of request payloads containing transform references, but also allows Unity to find the
        requested transform more efficiently by using the transform path directly.

        :param absolute_transform_path: Absolute transform path of the specified transform reference. This is passed
        in because it was already calculated earlier.

        :return: A list containing the sibling indices of this transform reference and all its ancestors.
        """
        # Construct a list containing the sibling indices of this transform reference and all its ancestors.
        indices = [self.sibling_index]
        parent = self.parent
        while parent is not None:
            indices.insert(0, parent.sibling_index)
            parent = parent.parent

        # If all sibling indices are -1, just return None. This not only decreases the size of the request payload,
        # but also allows Unity to find the requested transform more efficiently.
        if indices.count(-1) == len(indices):
            return None

        # Make sure the number of sibling indices matches the number of elements in transform_path.
        path_parts = absolute_transform_path.split('/')
        while len(indices) < len(path_parts):
            indices.insert(0, -1)

        return indices

    @staticmethod
    def to_payload(transform_ref):
        """
        Converts a transform reference to a request payload to be sent to the server.

        The resulting payload only contains the ``transform_path`` and ``sibling_indices`` attributes since that is
        sufficient to unambiguously specify transforms when sending requests to the server.

        :param transform_ref: The transform reference to convert.
        :return: A request payload representing the transform reference that can be sent to the server.
        """
        # Bail if there's nothing to convert.
        if transform_ref is None:
            return None

        # Make sure we have a valid transform reference to convert.
        if not isinstance(transform_ref, TransformRef):
            raise ValueError('transform_ref must be a type of TransformRef.')

        # Convert the transform reference to a serializable payload.
        #
        # NOTE: Because the request payload doesn't include parent information, we need to specify the absolute
        #       transform path so that Unity can find the requested transform.

        transform_path = transform_ref.get_absolute_transform_path()
        sibling_indices = transform_ref._get_sibling_indices(transform_path)

        payload = {
            "transform_path": transform_path,
            "sibling_indices": sibling_indices,
            "children": None,
            "parent": None
        }

        return payload

    @staticmethod
    def from_payload(payload, parent=None):
        """
        Converts a response payload received from the server to a transform reference.

        Response payloads don't include parent information, so an optional reference to a parent transform may be
        specified to complete the initialization of the returned transform reference.

        :param payload: The response payload to convert.
        :param parent: Optional reference to a parent transform.
        :return: A transform reference representing the payload that was received from the server.
        """
        # Bail if there's nothing to convert.
        if payload is None:
            return None

        # Make sure the parent transform reference is valid.
        if (parent is not None) and not isinstance(parent, TransformRef):
            raise ValueError("parent must be None or of type TransformRef")

        # Create the transform reference.
        transform_ref = TransformRef(payload['transform_path'], payload['sibling_indices'][0], parent)

        # Initialize the child transform references.
        if payload['children'] is not None:
            transform_ref.children = []
            for child_payload in payload['children']:
                TransformRef.from_payload(child_payload, transform_ref)

        return transform_ref

    @staticmethod
    def list_to_payload(transform_refs):
        """
        Converts a list of transform references to a request payload to be sent to the server.

        The resulting payload only contains the ``transform_path`` and ``sibling_indices`` attributes since that is
        sufficient to unambiguously specify transforms when sending requests to the server.

        :param transform_refs: The list of transform reference to convert.
        :return: A request payload representing the transform references that can be sent to the server.
        """
        # Bail if there's nothing to convert.
        if transform_refs is None:
            return None

        # Convert the transform references to a serializable payload.
        payload = []

        for transform_ref in transform_refs:
            transform_ref_payload = TransformRef.to_payload(transform_ref)
            payload.append(transform_ref_payload)

        return payload

    @staticmethod
    def list_from_payload(payload, parent=None):
        """
        Converts a response payload received from the server to a list of transform references.

        Response payloads don't include parent information, so an optional reference to a parent transform may be
        specified to complete the initialization of the returned transform references.

        :param payload: The response payload to convert.
        :param parent: Optional reference to a parent transform.
        :return: A list of transform references representing the payload that was received from the server.
        """
        # Bail if there's nothing to convert.
        if payload is None:
            return None

        # Make sure the parent transform reference is valid.
        if (parent is not None) and not isinstance(parent, TransformRef):
            raise ValueError("parent must be None or of type TransformRef")

        # Convert the payload to a list of transform references.
        transform_refs = []

        for transform_ref_payload in payload:
            transform_ref = TransformRef.from_payload(transform_ref_payload, parent)
            transform_refs.append(transform_ref)

        return transform_refs
