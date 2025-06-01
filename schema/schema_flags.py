# File Path: /src/schema/schema_flags.py

class SchemaState:
    """
    Class to track the current state of the schema.
    It includes flags for suppression and override triggers.
    """

    def __init__(self):
        # Default values for schema state
        self.suppression_active = False   # Flag to check if suppression is active
        self.override_trigger = None     # Store the current override trigger, if any

    def reset(self):
        """
        Resets the schema state, particularly the suppression and override trigger.
        """
        self.suppression_active = False  # Reset suppression flag
        self.override_trigger = None    # Reset override trigger
        print(f"[SchemaState] Reset schema state: {self}")

    def __repr__(self):
        """
        String representation for logging and debugging purposes.
        """
        return f"SchemaState(suppression_active={self.suppression_active}, override_trigger={self.override_trigger})"
