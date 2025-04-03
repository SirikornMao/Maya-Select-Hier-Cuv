import maya.cmds as cmds

# ฟังก์ชันสำหรับเลือก curve ที่อยู่ในกลุ่ม
def select_hierarchy_curves(groups):
    all_curves = []
    
    # สำหรับทุกๆ group ที่ได้รับ
    for group_name in groups:
        # หา children ที่เป็น curve ภายใน group
        curves_in_group = cmds.listRelatives(group_name, children=True, type='transform')
        
        if curves_in_group:
            for curve in curves_in_group:
                # ตรวจสอบว่าเป็น nurbsCurve (curve) หรือไม่
                if cmds.objectType(curve) == 'transform' and cmds.listRelatives(curve, type='nurbsCurve'):
                    all_curves.append(curve)

    # เลือก curve ทั้งหมดที่พบ
    if all_curves:
        cmds.select(all_curves)
    else:
        print("ไม่พบ curve ในกลุ่มที่ระบุ")

# ฟังก์ชันสร้าง UI ที่สามารถ custom ชื่อกลุ่มและจำนวนกลุ่มได้
def create_ui():
    if cmds.window("selectCurveWindow", exists=True):
        cmds.deleteUI("selectCurveWindow", window=True)

    # สร้างหน้าต่าง UI
    window = cmds.window("selectCurveWindow", title="Select Hierarchy Curves", widthHeight=(400, 300))

    cmds.columnLayout(adjustableColumn=True)
    
    # ส่วนกรอกชื่อกลุ่มและจำนวนกลุ่ม
    cmds.text(label="กรอกชื่อ Group และ Curve ตามจำนวนที่ต้องการ:")

    # ตัวแปรเพื่อเก็บจำนวนกลุ่มที่ต้องการ
    num_groups_field = cmds.intField(value=5)  # ใช้ intField แทน label
    
    # ส่วนสำหรับเก็บข้อมูลกลุ่มและ curve
    group_names = []
    curve_names = []
    group_fields = []
    curve_fields = []
    
    # ฟังก์ชันสร้างช่องกรอกกลุ่มและ curve
    def update_group_ui(*args):
        nonlocal group_fields, curve_fields
        
        # ลบช่องกรอกเดิมออก
        if group_fields:
            for field in group_fields:
                cmds.textFieldGrp(field, edit=True, text="")
        
        if curve_fields:
            for field in curve_fields:
                cmds.textFieldGrp(field, edit=True, text="")
        
        group_fields = []
        curve_fields = []
        
        num_groups = cmds.intField(num_groups_field, q=True, value=True)
        
        # สร้างช่องกรอกชื่อ group และ curve ตามจำนวนที่กำหนด
        for i in range(num_groups):
            group_field = cmds.textFieldGrp(label=f"Group {i + 1}", text="")
            curve_field = cmds.textFieldGrp(label=f"Curve {i + 1} for Group {i + 1}", text="")
            group_fields.append(group_field)
            curve_fields.append(curve_field)

    # อัพเดต UI เมื่อมีการเปลี่ยนแปลงจำนวนกลุ่ม
    cmds.intField(num_groups_field, edit=True, changeCommand=update_group_ui)
    
    # สร้างปุ่มสำหรับเลือก curve ที่อยู่ใน group ที่กรอกไว้
    def on_select_button_clicked(*args):
        selected_groups = []
        
        # รับค่าจากช่องกรอกชื่อกลุ่ม
        for group_field, curve_field in zip(group_fields, curve_fields):
            group_name = cmds.textFieldGrp(group_field, q=True, text=True)
            curve_name = cmds.textFieldGrp(curve_field, q=True, text=True)
            
            if group_name and curve_name:  # ถ้ามีชื่อกรอกเข้ามา
                selected_groups.append(group_name)
        
        # เรียกฟังก์ชันสำหรับเลือก curve ในกลุ่มที่เลือก
        select_hierarchy_curves(selected_groups)
    
    # ปุ่มสำหรับเลือก curve
    cmds.button(label="Select Curves", command=on_select_button_clicked)

    # อัพเดต UI เบื้องต้น
    update_group_ui()
    
    cmds.showWindow(window)

# เรียกใช้งาน UI
create_ui()
