import vmi
import numpy as np


def read_stl():
    file_name = vmi.askOpenFile('*.stl')
    if file_name is not None:
        poly_data = vmi.vtkread_STL(file_name)
        if poly_data.GetNumberOfCells() > 0:
            return poly_data


def LeftButtonPress(**kwargs):
    """响应左键按下"""
    if kwargs['picked'] is mesh_prop:
        pt = view.mouseOnPropCell()
        path_pts.clear()
        path_pts.append(pt)
        rebuild_path(path_pts)


def LeftButtonPressMove(**kwargs):
    """响应左键按下之后移动"""
    if kwargs['picked'] is mesh_prop:
        pt = view.mouseOnPropCell()
        rebuild_path([*path_pts, pt])
        if view.mouseOnProp() is mesh_prop:
            path_pts.append(pt)


def LeftButtonPressMoveRelease(**kwargs):
    """响应左键按下移动之后释放"""
    if kwargs['picked'] is mesh_prop:
        rebuild_plate()


def rebuild_path(pts):
    if len(pts) > 1:
        path_shape_data.clone(vmi.mkWire(vmi.mkSegments(pts)))
    else:
        path_shape_data.clone()
    view.updateInTime()


def rebuild_plate():
    if len(path_pts) > 1:
        cs = view.cameraCS()
        solids = []
        for center in [path_pts[0], path_pts[-1]]:
            h = plate_outer_radius  # 圆柱半高等于外半径
            end_center = [cs.mpt([0, 0, -h], origin=center),
                          cs.mpt([0, 0, h], origin=center)]
            end_wire = [vmi.mkWire(vmi.mkCircle_CS(end_center[0], plate_outer_radius + 1, cs)),
                        vmi.mkWire(vmi.mkCircle_CS(end_center[1], plate_outer_radius, cs))]
            end_face = [vmi.mkFace(end_wire[0]),
                        vmi.mkFace(end_wire[1])]
            profile = vmi.mkLoft([end_wire[0], end_wire[1]], True)
            solid = vmi.mkSolid(vmi.mkSew([end_face[0], end_face[1], profile]))

            plate_poly_data = vmi.mkPolyData_Shape(solid)
            plate_poly_data = vmi.poTriangle(plate_poly_data, 0, 0)

            plate_poly_data = vmi.poBoolean_Difference(plate_poly_data, mesh_poly_data)
            # plate_poly_data = vmi.poExtract_Largest(plate_poly_data)
            solids.append(plate_poly_data)

        plate_prop.clone(vmi.poAppend(solids))
        plate_prop.rep('wireframe')
        mesh_prop.visible(False)
    else:
        plate_prop.clone()
    view.updateInTime()


if __name__ == '__main__':
    from PySide2.QtWidgets import QAction

    mesh_poly_data = read_stl()  # 读取STL文件到单元数据
    if mesh_poly_data is None:
        vmi.appexit()

    view = vmi.View()  # 视图

    # 面网格模型
    mesh_prop = vmi.PolyActor(view)
    mesh_prop.color([1, 1, 0.6])  # 颜色
    mesh_prop.pickable(True)  # 设置可拾取+
    mesh_prop.mouse['LeftButton']['Press'] = LeftButtonPress
    mesh_prop.mouse['LeftButton']['PressMove'] = LeftButtonPressMove
    mesh_prop.mouse['LeftButton']['PressMoveRelease'] = LeftButtonPressMoveRelease
    mesh_prop.clone(mesh_poly_data)

    # 拾取路径
    path_pts = []
    path_shape_data = vmi.ShapeData()
    path_prop = vmi.PolyActor(view, shape_data=path_shape_data)
    path_prop.color([1, 0.4, 0.4])  # 颜色
    path_prop.size(line=3)

    # 导板
    plate_hole_axis = np.array([0, 0, 1])
    plate_outer_radius = 5
    plate_inner_radius = 1
    plate_prop = vmi.PolyActor(view)
    plate_prop.color([0.4, 0.6, 1])  # 颜色

    view.cameraFit()
    vmi.appexec(view)  # 执行主窗口程序
    vmi.appexit()  # 清理并退出程序
