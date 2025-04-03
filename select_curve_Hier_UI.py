import maya.cmds as cmds

# Function for selecting curves that are in the groups
def select_hierarchy_curves(groups):
    all_curves = []
    
    # For every group that receivesd
    for group_name in groups:
        # Find children who are curves within the group
        curves_in_group = cmds.listRelatives(group_name, children=True, type='transform')
        
        if curves_in_group:
            for curve in curves_in_group:
                # Check if it's nurbsCurve (curve)
                if cmds.objectType(curve) == 'transform' and cmds.listRelatives(curve, type='nurbsCurve'):
                    all_curves.append(curve)

    # Select all curves found
    if all_curves:
        cmds.select(all_curves)
    else:
        print("No curve found in the specified group")

# Create a UI that can customize the group name and number of groups
def create_ui():
    if cmds.window("selectCurveWindow", exists=True):
        cmds.deleteUI("selectCurveWindow", window=True)

    # Create UI Window
    window = cmds.window("selectCurveWindow", title="Select Hierarchy Curves", widthHeight=(400, 300))

    cmds.columnLayout(adjustableColumn=True)
    
    # Fill in the group name and number of groups
    cmds.text(label="Fill in the required number of Group and Curve names:")

    # variable to store the desired number of groups
    num_groups_field = cmds.intField(value=5)  # Use intField instead of label
    
    # Sections for collecting group and curve data
    group_names = []
    curve_names = []
    group_fields = []
    curve_fields = []
    
    # Function to create group and curve fields
    def update_group_ui(*args):
        nonlocal group_fields, curve_fields
        
        # Delete the original fields if they exist
        if group_fields:
            for field in group_fields:
                cmds.textFieldGrp(field, edit=True, text="")
        
        if curve_fields:
            for field in curve_fields:
                cmds.textFieldGrp(field, edit=True, text="")
        
        group_fields = []
        curve_fields = []
        
        num_groups = cmds.intField(num_groups_field, q=True, value=True)
        
        # Create a certain number of fields to fill in the group and curve names
        for i in range(num_groups):
            group_field = cmds.textFieldGrp(label=f"Group {i + 1}", text="")
            curve_field = cmds.textFieldGrp(label=f"Curve {i + 1} for Group {i + 1}", text="")
            group_fields.append(group_field)
            curve_fields.append(curve_field)

    # Update the UI when the number of groups changes
    cmds.intField(num_groups_field, edit=True, changeCommand=update_group_ui)
    
    # Create a button for selecting curves in the group that you have filled in
    def on_select_button_clicked(*args):
        selected_groups = []
        
        # Get the value from the group name fields and curve name fields
        for group_field, curve_field in zip(group_fields, curve_fields):
            group_name = cmds.textFieldGrp(group_field, q=True, text=True)
            curve_name = cmds.textFieldGrp(curve_field, q=True, text=True)
            
            if group_name and curve_name:  # If your name is filled in
                selected_groups.append(group_name)
        
        # Invoke the function for selecting curves in the selected groups
        select_hierarchy_curves(selected_groups)
    
    # Button for selecting curves
    cmds.button(label="Select Curves", command=on_select_button_clicked)

    # Initial UI Updates
    update_group_ui()
    
    cmds.showWindow(window)

# Run UI
create_ui()
