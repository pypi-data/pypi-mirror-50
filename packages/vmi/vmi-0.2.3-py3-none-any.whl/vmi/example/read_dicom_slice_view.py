def run():
    import vmi
    dcmdir = vmi.askDirectory()  # 用户选择文件夹

    if dcmdir is not None:  # 判断用户选中了有效文件夹并点击了确认
        series_list = vmi.sortSeries(dcmdir)  # 将文件夹及其子目录包含的所有DICOM文件分类到各个系列

        if len(series_list) > 0:  # 判断该文件夹内包含有效的DICOM系列
            series = vmi.askSeries(series_list)  # 用户选择DICOM系列
            image = series.read()  # 读取DICOM系列为图像数据

            view = vmi.View()  # 视图

            image_slice = vmi.ImageSlice(view)  # 断层图像
            image_slice.clone(image)  # 载入读取到的DICOM图像
            image_slice.slicePlane(face='axial', origin='center')  # 设置断层图像显示横断面，位置居中

            view.setCameraFit()  # 自动调整视图的视野范围
            vmi.appexec(view)  # 执行主窗口程序


if __name__ == '__main__':
    run()
