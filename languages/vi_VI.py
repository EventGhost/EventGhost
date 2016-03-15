# -*- coding: UTF-8 -*-
class General:
    apply = u"Cập nhật"
    autostartItem = u"Khởi động tự động"
    browse = u"Chọn"
    cancel = u"Hủy"
    choose = u"Chọn"
    configTree = u"Cây thiết lập"
    deleteLinkedItems = u"Có ít nhất 1 mục ngoài lựa chọn của bạn tham chiếu tới 1 mục trong lựa chọn của bạn. Nếu bạn tiếp tục xóa mục đã lựa chọn này, mục tham chiếu kia sẽ không hoạt động đúng.\n\nBạn có chắc xóa mục lựa chọn này? "
    deleteManyQuestion = u"Mục này có %s mục con.\nBạn có chắc là xóa tất cả?"
    deletePlugin = u"Plugin này được sử dụng bởi 1 action trong thiết lập của bạn.\nBạn không thể gỡ bỏ nó trước khi mọi action sử dụng plugin này được gỡ bỏ."
    deleteQuestion = u"Bạn có chắc xóa mục này"
    help = u"&Trợ Giúp"
    moreTag = u"Tiếp..."
    no = u"&Không"
    noOptionsAction = u"Action này không có thiết lập nào."
    noOptionsPlugin = u"Plugin này không có thiết lập nào."
    ok = u"OK"
    pluginLabel = u"Plugin: %s"
    settingsActionCaption = u"Các thiết lập Action"
    settingsEventCaption = u"Cấu hình Event"
    settingsPluginCaption = u"Cấu hình Plugin"
    test = u"&Thử trước"
    unnamedEvent = u"<event chưa có tên>"
    unnamedFile = u"<File chưa có tên>"
    unnamedFolder = u"<Folder chưa có tên>"
    unnamedMacro = u"<Macro chưa có tên>"
    yes = u"&Đúng"
class MainFrame:
    onlyLogAssigned = u"&Log chỉ sử dụng với các event được gán và kích hoạt ở cây thiết lập"
    onlyLogAssignedToolTip = u"Nếu chọn, khu vực log sẽ chỉ hiện lên những Event đang được thực hiện trong thiết lập hiện tại. Vì vậy bạn *không * nên chọn vào ô này trong khi bạn muốn gán 1 Event mới "
    class Logger:
        caption = u"Vùng Log các thao tác sự kiện"
        welcomeText = u"---> Chào mừng bạn đã vào chương trình Eventghost<---"
    class Menu:
        About = u"Thông tin về Eventghost"
        AddAction = u"Tạo thêm Action..."
        AddEvent = u"Tạo thêm Event..."
        AddFolder = u"Tạo thêm Folder..."
        AddMacro = u"Tạo thêm Macro..."
        AddPlugin = u"Tạo thêm Plugin..."
        Apply = u"Cập nhậy thay đổi"
        CheckUpdate = u"Cập nhật nâng cấp"
        ClearLog = u"Xóa Log"
        Close = u"&Đóng"
        CollapseAll = u"&Co lại tất cả"
        ConfigurationMenu = u"&Thiết lập"
        Configure = u"Thiết lập"
        Copy = u"&Copy"
        Cut = u"Cu&t"
        Delete = u"&Xóa"
        Disabled = u"Tắt"
        EditMenu = u"&Thao tác"
        Execute = u"Thực hiện"
        Exit = u"&Thoát"
        ExpandAll = u"&Mở ra tất cả"
        ExpandOnEvents = u"Chọn mục để thực hiện"
        Export = u"Xuất..."
        FileMenu = u"&File"
        Find = u"&Tìm..."
        FindNext = u"Tìm &Tiếp"
        HelpContents = u"&Nội dung trợ giúp"
        HelpMenu = u"&Trợ giúp"
        HideShowToolbar = u"Thanh công cụ"
        Import = u"Nhập từ nguồn khác..."
        IndentLog = u"Lùi dòng Log để dễ nhìn"
        LogActions = u"Log Actions"
        LogMacros = u"Log Macros"
        LogTime = u"Log Thời gian"
        New = u"&Mới"
        Open = u"&Mở..."
        Options = u"&Lựa chọn..."
        Paste = u"&Paste"
        PythonShell = u"Python Shell"
        Redo = u"&Redo"
        Rename = u"Đổi tên"
        Reset = u"Reset"
        Save = u"&Lưu"
        SaveAs = u"Lưu lại file &khác..."
        SelectAll = u"Chọn tất cả"
        Undo = u"&Undo"
        ViewMenu = u"Hiển thị"
        WebForum = u"&Forum trợ giúp"
        WebHomepage = u"Home &Page"
        WebWiki = u"&Wiki"
    class Messages:
        cantAddAction = u"Bạn không thể tạo thêm 1 Action tại đây.\nXin hãy chọn 1 Macro hoặc 1 vị trí trong 1 Macro mà bạn muốn Event được thêm vào"
        cantAddEvent = u"Bạn không thể tạo thêm 1 Event tại đây.\n\nHãy chọn 1 Macro  mà bạn muốn Event được thêm vào."
        cantConfigure = u"Bạn không thể thiết lập mục này\n\nChỉ có Action, Event và Plugin mới thay đổi được thiết lập."
        cantDisable = u"Mục gốc và mục Khởi động tự động không thể bị vô hiệu."
        cantExecute = u"Mục gốc, các mục Folder và Event không thể thực hiện gì."
        cantRename = u"Chỉ có Folder, Macro và Action có thể đổi tên"
    class SaveChanges:
        dontSaveButton = u"&Không Lưu"
        mesg = u"File đã bị thay đổi.\n\nBạn có muốn lưu lại những thay đổi này?"
        saveButton = u"&Lưu"
    class TaskBarMenu:
        Exit = u"Thoát"
        Hide = u"Ẩn EventGhost"
        Show = u"Hiện EventGhost"
    class Tree:
        caption = u"Vùng thiết lập"
class Error:
    FileNotFound = u'Không tìm thấy file "%s"'
    InAction = u'Lỗi trong Action: "%s"'
    configureError = u"Lỗi khi thiết lập : %s"
    pluginLoadError = u"Lỗi khi nạp file plugin %s"
    pluginNotActivated = u'Plugin "%s" chưa được kích hoạt'
    pluginStartError = u"Lỗi khởi động plugin: %s"
class Exceptions:
    DeviceInitFailed = u"Không thể khởi động thiết bị!"
    DeviceNotFound = u"Không tìm thấy thiết bị!"
    DeviceNotReady = u"Thiết bị chưa sẵn sàng!"
    DriverNotFound = u"Không tìm thấy driver!"
    DriverNotOpen = u"Không thể mở driver!"
    InitFailed = u"Quá trình khởi động bị lỗi!"
    PluginLoadError = u"Nạp plugin lỗi!"
    PluginNotFound = u"Không tìm thấy plugin!"
    ProgramNotFound = u"Không tìm thấy chương trình!"
    ProgramNotRunning = u"Chương trình chưa chạy!"
    SerialOpenFailed = u"Không thể mở cổng Serial!"
class CheckUpdate:
    ManErrorMesg = u"Không thể lấy được thông tin trên website của EventGhost\n\nXin vui lòng thử lại."
    ManOkMesg = u"Hiện tại chưa có phiên bản Eventghost nào mới hơn"
    downloadButton = u"Truy cập trang Download"
    newVersionMesg = u"Eventghost vừa nâng cấp phiên bản mới!\n\n                Phiên bản hiện tại: %s\n                Phiên bản mới nhất: %s\n\nBạn có muốn truy cập web để tải về?"
    waitMesg = u"Xin vui lòng đợi trong lúc Eventghost thu thập các thông tin để nâng cấp."
class AddActionDialog:
    descriptionLabel = u"Mô tả"
    title = u"Chọn 1 Action để thêm vào..."
class AddPluginDialog:
    author = u"Tác giả:"
    descriptionBox = u"Mô tả"
    externalPlugins = u"Liên kết ngoài"
    noInfo = u"Không có thông tin nào tồn tại."
    noMultiload = u"Plugin này không hỗ trợ chạy đồng thời và bạn đã có sẵn plugin này đang chạy trong thiết lập của bạn."
    noMultiloadTitle = u"Không thể chạy đồng thời"
    otherPlugins = u"Khác"
    programPlugins = u"Điều khiển chương trình"
    remotePlugins = u"Bộ thu tín hiệu remote"
    title = u"Chọn một plugin để thêm vào..."
    version = u"Phiên bản:"
class AddActionGroupDialog:
    caption = u"Thêm Actions?"
    message = u"EventGhost có thể thêm một folder với tất cả action của plugin này vào cây thiết lập. Nếu bạn muốn làm vậy, chọn 1 vị trí để thêm vào và ấn OK.\n\nTrong trường hợp ngược lại bạn ấn nút Hủy."
class EventItem:
    eventItem = u"Event"
    eventName = u"Tên Event:"
    notice = u"Chú ý: Bạn có thể kéo và thả các Event từ khu vực Log vào một Macro"
class OptionsDialog:
    CheckUpdate = u"Kiểm tra cập nhật phiên bản mới lúc khởi động"
    HideOnClose = u"Thu nhỏ xuống khay hệ thống khi đóng cửa sổ"
    HideOnStartup = u"Ẩn khi khởi động"
    LanguageGroup = u"Ngôn ngữ"
    StartGroup = u"Lúc khởi động"
    StartWithWindows = u"Tự động khởi động Eventghost cùng hệ thống"
    Tab1 = u"Tổng quát"
    Title = u"Các lựa chọn"
    UseAutoloadFile = u"Tự động nạp file"
    Warning = u"Ngôn ngữ sẽ thay đổi sau khi bạn khởi động lại chương trình"
    confirmDelete = u"Xác nhận xóa nhánh cây thiết lập"
    limitMemory1 = u"Giới hạn sử dụng bộ nhớ khi ở trạng thái thu nhỏ về"
    limitMemory2 = u"MB"
class FindDialog:
    caseSensitive = u"&Tìm chính xác"
    direction = u"Hướng tìm"
    down = u"$Xuống"
    findButton = u"&Tìm tiếp"
    notFoundMesg = u'Không tìm thấy "%s".'
    searchLabel = u"Tìm &kiếm:"
    searchParameters = u"Tìm với những thông số sau"
    title = u"Tìm"
    up = u"&Lên"
    wholeWordsOnly = u"Tìm toàn &bộ từ"
class AboutDialog:
    Author = u"Tác giả: %s"
    CreationDate = u"%a, %d %b %Y %H:%M:%S"
    Title = u"Thông tin về EventGhost"
    Version = u"Phiên bản: %s (build %s)"
    tabAbout = u"Thông tin"
    tabChangelog = u"Cập nhật"
    tabLicense = u"Thỏa thuận bản quyền"
    tabSpecialThanks = u"Chân thành cảm ơn "
    tabSystemInfo = u"Thông tin hệ thống"
class Plugin:
    class EventGhost:
        name = u"EventGhost"
        description = u"Tại đây bạn có thể tìm thấy các action điều khiển các chức năng của EventGhost"
        class AutoRepeat:
            name = u"Tự động lặp lại macro hiện tại"
            description = u"Tạo macro để những lệnh này được thêm vào một macro tự động lặp lại."
            seconds = u"thứ hai"
            text1 = u"Bắt đầu lặp lại lần thứ nhất sau"
            text2 = u"với  1 lặp lại mỗi"
            text3 = u"Tăng thêm sự lặp lại sau"
            text4 = u"đến 1 lặp lại mỗi"
        class Comment:
            name = u"Chú thích"
            description = u"Đây là chú thích cho các lệnh của bạn - không có tác dụng thực hiện lệnh gì cả."
        class DisableItem:
            name = u"Tắt"
            description = u"Vô hiệu hóa 1 mục"
            cantSelect = u"Mục bạn chọn không thể thay đổi trạng thái đang kích hoạt của nó.\n\nXin hãy chọn mục khác."
            label = u"Tắt: %s"
            text1 = u"Vui lòng chọn mục sẽ được vô hiệu hóa:"
        class EnableExclusive:
            name = u"Loại trừ kích hoạt một Folder/Macro"
            description = u"Mục này có tác dụng kích hoạt 1 Folder hoặc 1 Macro nào đó trong thiết lập của bạn, nhưng đồng thời tắt tất cả những Folder hoặc Macro khác mà nằm chung 1 nhánh trên cây thiết lập với Folder(Macro) cần kích hoạt."
            cantSelect = u"Mục bạn chọn không thể thay đổi trạng thái đang kích hoạt của nó.\n\nXin hãy chọn mục khác."
            label = u"Kích hoạt loạt trừ : %s"
            text1 = u"Vui lòng chọn folder/macro sẽ được kích hoạt:"
        class EnableItem:
            name = u"Kích hoạt 1 mục"
            description = u"Kích hoạt 1 mục trên cây thiết lập"
            cantSelect = u"Mục bạn chọn không thể thay đổi trạng thái đang kích hoạt của nó.\n\nXin hãy chọn mục khác."
            label = u"Kích hoạt: %s"
            text1 = u"Vui lòng chọn mục sẽ được kích hoạt:"
        class FlushEvents:
            name = u"Xóa những Event đang chờ lệnh"
            description = u'<rst>\n        Mục này sẽ xóa tất cả những Event đang chờ thực hiện.\n        \n        Sử dụng hữu dụng trong trường hợp 1 macro có quá trình thực hiện lệnh quá lâu\n        và các event phải chờ thực hiện quá lâu thì nên dừng luôn\n        \n        **Ví dụ:** Bạn có 1 macro "Khởi động hệ thống" cần thực hiện tới 90 giây. Người dùng\n        cuối sẽ không nhìn thấy gì khi máy chiếu bật sáng mà quá trình này mất 60 giây. Rất có \n        khả năng anh ta sẽ dùng remote ấn thêm vài lần và như vật macro này sẽ được kích hoạt\n        vài lần, khiến cho quá trình thực hiện lệnh dài ra do liên tục bắt đầu khởi động. Nếu bạn\n        cho một lệnh "Xóa các event đang chờ thực hiện" vào cuối macro của bạn, tất cả những\n        thao tác ấn nút remote thừa sẽ bị bỏ qua.\n    '
        class JumpIfLongPress:
            name = u"Nhảy đến 1 vị trí nếu ấn giữ trong thời gian dài"
            description = u"Nhảy đến 1 macro khác, nếu nút trên remote được ấn giữ lâu hơn thời gian đã được thiết lập"
            label = u"Nếu nút được ấn giữ trong vòng %s giây, nhảy đến %s"
            text1 = u"Nếu nút được ấn giữ lâu hơn"
            text2 = u"giây,"
            text3 = u"nhảy đến:"
            text4 = u"Chọn macro ấn giữ lâu..."
            text5 = u"Vui lòng chọn macro sẽ được kích hoạt nếu event là 1 event dài."
        class NewJumpIf:
            name = u"Nhảy"
            description = u"Nhảy đến 1 macro khác nếu thỏa mãn điều kiện"
            choices = [
                u"Action cuối thực hiện thành công",
                u"Action cuối thực hiện không thành công",
                u"luôn luôn",
            ]
            labels = [
                u'Nếu thành công nhảy tới "%s"',
                u'Nếu không thành công nhảy tới "%s"',
                u'Nhảy tới "%s"',
                u'Nếu thành công nhảy tới "%s" và quay lại',
                u'Nếu không thành công nhảy tới "%s"',
                u'Nhảy tới "%s" và quay lại',
            ]
            mesg1 = u"Chọn macro..."
            mesg2 = u"Vui lòng chọn macro sẽ thực thi khi thỏa mãn điều kiện"
            text1 = u"Nếu:"
            text2 = u"Nhảy tới:"
            text3 = u"và quay lại sau khi thực hiện"
        class PythonCommand:
            name = u"Lệnh Python"
            description = u"Thực hiện một lệnh Python đơn."
            parameterDescription = u"Câu lệnh Python:"
        class PythonScript:
            name = u"Python Script"
            description = u"Full featured Python script."
        class ShowOSD:
            name = u"Hiện OSD"
            description = u"Hiện lên 1 vùng (dòng) hiển thị lên màn hình( On Screen Display)."
            alignment = u"Căn chỉnh vị trí"
            alignmentChoices = [
                u"Phía trên bên trái",
                u"Phía trên bên phải",
                u"Phía dưới bên trái",
                u"Phía dưới bên phải",
                u"Trung tâm màn hình",
                u"Phía dưới vùng trung tâm",
                u"Phía trên vùng trung tâm",
                u"Phía trái vùng trung tâm",
                u"Phía phải vùng trung tâm",
            ]
            display = u"Hiển thị trên màn hình:"
            editText = u"Chữ hiển thị:"
            label = u"Hiện OSD: %s"
            osdColour = u"Màu chữ:"
            osdFont = u"Font chữ:"
            outlineFont = u"Đường bao ngoài OSD"
            skin = u"Sử dụng skin"
            wait1 = u"Tự động ẩn OSD sau"
            wait2 = u"giây (0 = never)"
            xOffset = u"Horizontal offset X:"
            yOffset = u"Vertical offset Y:"
        class StopProcessing:
            name = u"Dừng thực hiện event này"
            description = u"Sau action này, Eventghost sẽ không thực hiện các macro của event đã được xử lý"
        class TriggerEvent:
            name = u"Kích hoạt Event"
            description = u"khiến 1 event được tạo ra(sau 1 khoảng thời gian)"
            labelWithTime = u'Kích hoạt event "%s" sau %.2f giây'
            labelWithoutTime = u'Kích hoạt event "%s"'
            text1 = u"Chuỗi Event kích hoạt:"
            text2 = u"Độ trễ kích hoạt event:"
            text3 = u"giây. (0= ngay lập tức)"
        class Wait:
            name = u"Đợi 1 khoảng thời gian"
            description = u"Đợi 1 khoảng thời gian"
            label = u"Đợi : %s giây"
            seconds = u"giây"
            wait = u"Đợi"
    class System:
        name = u"Hệ thống"
        description = u"Điều khiển mọi chức năng hệ thống của bạn như card sound, đồ họa, quản lý điện..."
        forced = u"Cưỡng buộc: %s"
        forcedCB = u"Cưỡng buộc đóng mọi chương trình"
        class ChangeDisplaySettings:
            name = u"Thay đổi thiết lập màn hình"
            description = u"Thay đổi thiết lập màn hình"
            colourDepth = u"Độ sâu màu:"
            display = u"Hiển thị:"
            frequency = u"Tần số:"
            includeAll = u"Bao gồm cả những chế độ màn hình không hỗ trợ."
            label = u"Thay đổi màn hình%d sang chế độ %dx%d@%d Hz"
            resolution = u"Độ phân giải:"
            storeInRegistry = u"Lưu chế độ vào registry."
        class ChangeMasterVolumeBy:
            name = u"Thay đổi Master Volume"
            description = u"Thay đổi âm lượng tổng từ thông số hiện tại."
            text1 = u"Thay đổi âm lượng tổng"
            text2 = u"phần trăm(%)"
        class Execute:
            name = u"Chạy ứng dụng"
            description = u"Chạy 1 file exe"
            FilePath = u"Chạy file:"
            Parameters = u"Thông số kèm theo nếu có(command line):"
            ProcessOptions = (
                u"Thời gian thực",
                u"Hơn mức bình thường",
                u"Bình thường",
                u"dưới mức bình thường",
                u"Nghỉ",
            )
            ProcessOptionsDesc = u"Mức ưu tiên"
            WaitCheckbox = u"Đợi đến khi ứng dụng được đóng trước khi thực hiện"
            WindowOptions = (
                u"Cửa sổ bình thường",
                u"Thu nhỏ",
                u"Phóng to",
                u"Ẩn",
            )
            WindowOptionsDesc = u"Lựa chọn trạng thái cửa sổ:"
            WorkingDir = u"Thư mục:"
            browseExecutableDialogTitle = u"Chọn file exe"
            browseWorkingDirDialogTitle = u"Chọn thư mục"
            label = u"Khởi động chương trình: %s"
        class Hibernate:
            name = u"Ngủ đông PC"
            description = u"Chức năng này sẽ làm hệ thống nghỉ bằng cách tắt máy vào trạng thái hibernation (S4)"
        class LockWorkstation:
            name = u"Khóa máy"
            description = u"Chức năng khóa màn hình máy tính bảo vệ xâm nhập trái phép."
        class LogOff:
            name = u"Log-off tài khoản người dùng hiện tại"
            description = u"Đóng tất cả các chương trình đang thực hiện và đăng xuất."
        class MonitorGroup:
            name = u"Màn hình"
            description = u"Action này điều khiển trạng thái điện của màn hình PC."
        class MonitorPowerOff:
            name = u"Tắt màn hình"
            description = u"Tắt màn hình vào chế độ tiết kiệm điện"
        class MonitorPowerOn:
            name = u"Bật màn hình"
            description = u"Bật lại màn hình nếu ở trạng thái tắt hoặc dừng trình bảo vệ màn hình."
        class MonitorStandby:
            name = u"Thiết lập màn hình vào chế độ nghỉ(stand-by mode)"
            description = u"Đặt màn hình vào chế độ tiêu thụ năng lượng thấp."
        class MuteOff:
            name = u"Tắt chế độ câm lặng"
            description = u"Tắt chế độ câm lặng"
        class MuteOn:
            name = u"Bật chế độ câm lặng"
            description = u"Bật chế độ câm lặng"
        class OpenDriveTray:
            name = u"Đóng/Mở khay ổ đĩa"
            description = u"Điều khiển khay đĩa của ổ CD/DVD"
            driveLabel = u"Ổ chỉ định:"
            labels = [
                u"Đảo trạng thái khay ổ đĩa: %s",
                u"Mở khay ổ đĩa: %s",
                u"Đóng khay ổ đĩa: %s",
            ]
            options = [
                u"Đảo trạng thái đóng và mở của khay ổ đĩa",
                u"Chỉ mở khay ổ đĩa",
                u"Chỉ đóng khay ổ đĩa",
            ]
            optionsLabel = u"Chọn action"
        class PlaySound:
            name = u"Chơi file âm thanh"
            description = u"Chơi file âm thanh"
            fileMask = u"Wav-Files (*.WAV)|*.wav|All-Files (*.*)|*.*"
            text1 = u"Đường dẫn file:"
            text2 = u"Đợi để thực hiện xong"
        class PowerDown:
            name = u"Tắt PC"
            description = u"Shutdow hệ thống và tắt máy."
        class PowerGroup:
            name = u"Quản lý điện năng"
            description = u"Những action này sẽ làm tạm nghỉ, ngủ đông, khởi động lại, tắt máy. Cũng có thể khóa máy hoặc đăng xuất tài khoản người dùng hiện tại."
        class Reboot:
            name = u"Khởi động lại máy tính"
            description = u"Shutdown hệ thống và khởi động lại."
        class RegistryChange:
            name = u"Thay đổi giá trị Registry"
            description = u"Thay đổi giá trị của registry trong windows"
            actions = (
                u"tạo mới hoặc thay đổi",
                u"thay đổi nếu chỉ tồn tại",
                u"xóa",
            )
            labels = (
                u'Thay đổi "%s"  đến %s',
                u'Thay đổi "%s"  đến %s nếu chỉ tồn tại',
                u'Xóa "%s"',
            )
        class RegistryGroup:
            name = u"Registry"
            description = u"Truy vấn hoặc thay đổi giá trị trong Registry"
            actionText = u"Action:"
            chooseText = u"Chọn Registry Key: "
            defaultText = u"(Mặc định)"
            keyOpenError = u"Lỗi mở registry key"
            keyText = u"Key:"
            keyText2 = u"Key"
            newValue = u"Giá trị mới:"
            noKeyError = u"Không có key xác định"
            noNewValueError = u"Không có giá trị xác định"
            noSubkeyError = u"Không có subkey xác định"
            noTypeError = u"Không có loại xác định"
            noValueNameError = u"Không giá trị tên xác định"
            noValueText = u"Không tìm thấy giá trị"
            oldType = u"Kiểu hiện tại:"
            oldValue = u"Giá trị hiện tại:"
            typeText = u"Kiểu:"
            valueChangeError = u"Lỗi khi thay đổi giá trị"
            valueName = u"Tên giá trị:"
            valueText = u"Giá trị:"
        class RegistryQuery:
            name = u"Truy vấn Registry"
            description = u"Truy vấn Registry và trả về giá trị hoặc so sánh với giá trị"
            actions = (
                u"kiểm tra nếu tồn tại",
                u"trả về kết quả",
                u"so sánh với",
            )
            labels = (
                u'Kiểm tra nếu "%s" tồn tại',
                u'Trả về "%s" như kết quả',
                u'So sánh "%s" với %s',
            )
        class ResetIdleTimer:
            name = u"Thiết lập lại bộ đếm trạng thái nghỉ"
            description = u"Thiết lập lại bộ đếm trạng thái nghỉ"
        class SetClipboard:
            name = u"Copy chuỗi vào clipboard"
            description = u"Copy chuỗi thông số vào clipboard hệ thống"
            error = u"Không thể mở clipboard"
        class SetDisplayPreset:
            name = u"Thiết lập sẵn màn hình"
            description = u"Các thiết lập sẵn cho màn hình"
            fields = (
                u"Thiết bị",
                u"Trái",
                u"Trên",
                u"Chiều rộng",
                u"Chiều cao",
                u"Tần sô",
                u"Độ sâu màu",
                u"Gắn vào",
                u"Chính",
                u"Flags",
            )
            query = u"Truy vấn các thiết lập màn hình"
        class SetIdleTime:
            name = u"Thiết lập bộ đếm trạng thái nghỉ"
            description = u"Thiết lập bộ đếm trạng thái nghỉ"
            label1 = u"Đợi"
            label2 = u"giây trước khi kích hoạt event trạng thái nghỉ."
        class SetMasterVolume:
            name = u"Thiết lập Master Volume"
            description = u"Thiết lập âm lượng tổng từ đến 1 giá trị cố định."
            text1 = u"Thiết lập Master Volume đến"
            text2 = u"phần trăm(%)."
        class SetSystemIdleTimer:
            name = u"Thiết lập bộ đếm trạng thái nghỉ hệ thống"
            description = u"Thiết lập bộ đếm trạng thái nghỉ hệ thống"
            choices = [
                u"Tắt bộ đếm trạng thái nghỉ hệ thống",
                u"Kích hoạt bộ đếm trạng thái nghỉ hệ thống",
            ]
            text = u"Lựa chọn:"
        class SetWallpaper:
            name = u"Đổi ảnh nền Wallpaper"
            description = u"Đổi ảnh nền Wallpaper"
            choices = (
                u"Trung tâm",
                u"Xếp lớp",
                u"Giãn cho vừa màn hình",
            )
            fileMask = u"All Image Files|*.jpg;*.bmp;*.gif;*.png|All Files (*.*)|*.*"
            text1 = u"Đường dẫn đến file ảnh:"
            text2 = u"Căn chỉnh"
        class ShowPicture:
            name = u"Hiển thị 1 bức ảnh"
            description = u"Hiển thị 1 bức ảnh lên màn hình"
            allFiles = u"Tất cả các file"
            allImageFiles = u"Tất cả các file ảnh"
            display = u"Màn hình"
            path = u"Đường dẫn đến ảnh (để trống nếu xóa):"
        class SoundGroup:
            name = u"Card âm thanh"
            description = u"Những action điều khiển Card âm thanh của PC"
        class Standby:
            name = u"Stand By( Nghỉ PC)"
            description = u"Chức năng này sẽ tắt máy vào trạng thái nghỉ."
        class StartScreenSaver:
            name = u"Bật trình bảo vệ màn hình của windows"
            description = u"Bật trình bảo vệ màn hình đã được chọn sẵn"
        class ToggleMute:
            name = u"Đảo trạng thái của chế độ câm lặng"
            description = u"Đảo chế độ câm lặng từ không sang có hoặc ngược lại"
        class WakeOnLan:
            name = u"Wake on LAN"
            description = u"Đánh thức 1 PC khác thông qua 1 gói tin gửi qua mạng LAN"
            parameterDescription = u"Địa chỉ MAC của máy cần đánh thức:"
    class Window:
        name = u"Cửa sổ"
        description = u"Những action liên quan đến điều khiển các của sổ trên desktop như tìm 1 cửa sổ xác định, di chuyển, thay đổi kích cỡ và gửi 1 phím bấm đến cửa sổ đó."
        class BringToFront:
            name = u"Cho lên trên cùng"
            description = u"Cho 1 cửa sổ xác định lên trên cùng các cửa sổ khác."
        class Close:
            name = u"Đóng"
            description = u"Đóng cửa sổ chương trình ứng dụng"
        class FindWindow:
            name = u"Tìm 1 cửa sổ"
            description = u'Tìm 1 cửa sổ để về sau có thể sử dụng như một đối tượng của action nào đó trong macro.\n<p> Nếu 1 macro không có action "Tìm 1 cửa sổ", tất cả các action trong đó sẽ lấy đối tượng là cửa sổ trên cùng.<p>Trong hộp sửa đổi bạn có thể sử dụng dấu {*} để chọn bất kì từ nào và {?} để chọn 1 từ đơn lẻ.'
            drag1 = u"Kéo cái này\nvào 1 cửa sổ."
            drag2 = u"Di chuyển cái này\nvào 1 cửa sổ."
            hide_box = u"Ẩn EventGhost khi kéo"
            invisible_box = u"Tìm cả các mục ẩn"
            label = u"Tìm cửa sổ: %s"
            label2 = u"Tìm cửa sổ trên cùng"
            matchNum1 = u"Chỉ trả về \nkết quả thứ"
            matchNum2 = u"(Only return ?? 'th match)\n"
            onlyFrontmost = u"Chỉ khớp với cửa sổ trên cùng"
            options = (
                u"Chương trình:",
                u"Tên cửa sổ:\n",
                u"Window Class:",
                u"Child Name:",
                u"Child Class:",
            )
            refresh_btn = u"&Refresh"
            stopMacro = [
                u"Dừng macro nếu đối tượng không tìm thấy",
                u"Dừng macro nếu đối tượng được tìm thấy",
                u"Không bao giờ dừng macro",
            ]
            testButton = u"Kiểm tra"
            wait1 = u"Đợi đến"
            wait2 = u"giây để cửa sổ xuất hiện"
        class Maximize:
            name = u"Phóng to"
            description = u"Phóng to"
        class Minimize:
            name = u"Thu nhỏ"
            description = u"Thu nhỏ"
        class MoveTo:
            name = u"Di chuyển đến điểm xác định"
            description = u"Di chuyển đến điểm xác định"
            label = u"Di chuyển cửa sổ đến %s"
            text1 = u"Điểm X trên trục nằm ngang"
            text2 = u"pixels"
            text3 = u"Điểm Y trên trục thẳng đứng"
            text4 = u"pixels"
        class Resize:
            name = u"Đổi lại kích cỡ"
            description = u"Đổi lại kích cỡ của cửa sổ về 1 kích cỡ xác định"
            label = u"Đổi kích cỡ cửa sổ về %s, %s"
            text1 = u"Đổi chiều rộng về"
            text2 = u"pixels"
            text3 = u"Đổi chiều cao về"
            text4 = u"pixels"
        class Restore:
            name = u"Phục hồi cửa sổ"
            description = u"Phục hồi cửa sổ"
        class SendKeys:
            name = u"Giả lập gõ phím"
            description = u"<rst>\nAction này giả lập gõ phím để điều khiển các chương trình khác. Chỉ cần gõ kí tự bạn muốn vào ô sửa đổi.\n\nĐể giả lập phím đặc biệt, bạn phải để từ khóa của phím đó trong {}. Ví dụ nếu bạn muốn phím mũi tên lên, điền **{Up}**. Bạn có thể kết hợp nhiều phím bằng cách sử dụng kí tự + để gõ liền 1 lúc, ví dụ: **{Shift+Ctrl+F1}** or **{Ctrl+V}**."
            insertButton = u"&Thêm"
            specialKeyTool = u"Công cụ phím đặc biệt"
            textToType = u"Phím gõ:"
            useAlternativeMethod = u"Sửa dụng phương pháp khác để giả lập ấn phím"
            class Keys:
                backspace = u"Backspace"
                context = u"Context menu key"
                delete = u"Delete"
                down = u"Down"
                end = u"End"
                enter = u"Enter"
                escape = u"Escape"
                home = u"Home"
                insert = u"Insert"
                left = u"Left"
                num0 = u"Numpad 0"
                num1 = u"Numpad 1"
                num2 = u"Numpad 2"
                num3 = u"Numpad 3"
                num4 = u"Numpad 4"
                num5 = u"Numpad 5"
                num6 = u"Numpad 6"
                num7 = u"Numpad 7"
                num8 = u"Numpad 8"
                num9 = u"Numpad 9"
                numAdd = u"Numpad +"
                numDecimal = u"Numpad ."
                numDivide = u"Numpad /"
                numMultiply = u"Numpad *"
                numSubtract = u"Numpad -"
                pageDown = u"Page Down"
                pageUp = u"Page Up"
                returnKey = u"Return (Enter)"
                right = u"Right"
                space = u"Space"
                tabulator = u"Tab"
                up = u"Up"
                win = u"Phím Windows "
        class SendMessage:
            name = u"Gửi Message"
            description = u"Sử dụng hàm Windows-API SendMessage để gửi message đến 1 cửa sổ. Có thể sử dụng PostMessage nếu muốn."
            text1 = u"Sử dụng PostMessage thay thế SendMessage"
        class SetAlwaysOnTop:
            name = u"Luôn hiện ở trên cùng (always on top)"
            description = u"Thiết lập đặc tính Luôn hiện ở trên cùng (always on top) cho cửa sổ"
            actions = (
                u"Xóa đặc tính Luôn hiện ở trên cùng (always on top)",
                u"Thiết lập Luôn hiện ở trên cùng (always on top)",
                u"Đảo trạng thái đặc tính Luôn hiện ở trên cùng (always on top)",
            )
            radioBox = u"Chọn action:"
    class Mouse:
        name = u"Chuột"
        description = u"Cung cấp những Action để điều khiển con trỏ chuột và các Event giả lập chuột"
        class GoDirection:
            name = u"Di Chuột về một hướng"
            description = u"Di Chuột về một hướng nào đó "
            label = u"Di Chuột về hướng %.2f°"
            text1 = u"Di con trỏ Chuột về hướng"
            text2 = u"độ. (0-360)"
        class LeftButton:
            name = u"Nút trái chuột"
            description = u"Nút trái chuột"
        class LeftDoubleClick:
            name = u"Click đúp nút trái chuột"
            description = u"Click đúp nút trái chuột"
        class MiddleButton:
            name = u"Nút giữa chuột"
            description = u"Nút giữa chuột"
        class MouseWheel:
            name = u"Nút cuộn chuột"
            description = u"Dùng nút cuộn chuột"
            label = u"Bấm nút cuộn chuột %d click"
            text1 = u"Bấm nút cuộn chuột"
            text2 = u"Click. (Negative values turn down)"
        class MoveAbsolute:
            name = u"Di chuyển chuột đến điểm tuyệt đối"
            description = u"Di chuyển chuột đến điểm tuyệt đối"
            label = u"Di chuột đến điểm x:%s, y:%s"
            text1 = u"Điểm X trên trục nằm ngang:"
            text2 = u"pixels"
            text3 = u"Điểm Y trên trục thẳng đứng:"
            text4 = u"pixels"
        class MoveRelative:
            name = u"Di chuyển chuột đến điểm tương đối"
            description = u"Di chuyển chuột đến điểm tương đối"
            label = u"Thay đổi vị trí chuột tại x:%s, y:%s"
            text1 = u"Thay đổi điểm X trên trục ngang"
            text2 = u"pixels"
            text3 = u"Thay đổi điểm X trên trục thẳng đứng"
            text4 = u"pixels"
        class RightButton:
            name = u"Nút phải chuột"
            description = u"Nút phải chuột"
        class RightDoubleClick:
            name = u"Click đúp nút phải chuột"
            description = u"Click đúp nút phải chuột"
        class ToggleLeftButton:
            name = u"Thay đổi nút trái chuột"
            description = u"Thay đổi nút trái chuột"
    class BSPlayer:
        name = u"BSPlayer"
        description = u"Hỗ trợ chức năng điều khiển phần mềm BSPlayer"
    class Batto_IR:
        name = u"Batto IR"
        description = u"Plugin cho các dòng sản phẩm công nghệ IR của Batto."
    class Keyboard:
        name = u"Bàn phím"
        description = u"Plugin này tạo các Event ấn phím trên bàn phím (phím tắt - hotkey).\n\n**Chú ý:**Nếu một Event bàn phím được gắn vào một macro, Plugin này sẽ chặn phím bấm này, vì thế Windows hoặc những ứng dụng khác sẽ không nhận được phím này. Điều này là cần thiết vì những phím bấm sẽ được phép thay đổi, nếu không những phím cũ nếu dùng sẽ bị lặp và kích hoạt các action khác mà bạn muốn và thường thì đây không phải dự định của bạn.\n\nSự chặn phím bấm này chỉ xảy ra nếu 1 macro được thực hiện thành công với Event. Vì thế nếu macro hoặc bất kì nhánh mẹ của nó bị tắt, phím bấm vẫn có hiệu lực. "
