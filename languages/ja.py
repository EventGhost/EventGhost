# -*- coding: UTF-8 -*-
class General:
    apply = u"適用"
    autostartItem = u"自動実行"
    browse = u"閲覧..."
    cancel = u"キャンセル"
    choose = u"選択"
    configTree = u"ツリー設定"
    deleteLinkedItems = u"選択したアイテムを参照している他のアイテムが少なくとも１つ以上あります。もしそれを削除すると、参照しているアイテムが正常に動作しない場合があります。\n\n本当に選択したアイテムを削除しますか？"
    deleteManyQuestion = u"このエレメントには%s個のサブエレメントがあります。\n本当にすべてのエレメントを削除しますか？"
    deletePlugin = u"このプラグインは、設定でアクションとして使われています。\nこのプラグインが使われているすべてのアクションを削除しないと、このプラグインを削除できません。"
    deleteQuestion = u"本当にこのアイテムを削除しますか？"
    help = u"ヘルプ"
    moreTag = u"詳しくは..."
    noOptionsAction = u"このアクションはオプション設定がありません"
    noOptionsPlugin = u"このプラグインはオプション設定がありません"
    ok = u"OK"
    pluginLabel = u"プラグイン: %s"
    test = u"テスト"
    unnamedEvent = u"<名称未設定のイベント>"
    unnamedFile = u"<名称未設定のファイル>"
    unnamedFolder = u"<名称未設定のフォルダ>"
    unnamedMacro = u"<名称未設定のマクロ>"
class MainFrame:
    onlyLogAssigned = u"割り当てられたイベントで起動されたものだけログ表示する"
    class Logger:
        caption = u"ログ"
        descriptionHeader = u"説明"
        timeHeader = u"時間"
        welcomeText = u"--> ようこそEventGhostへ <--"
    class Menu:
        About = u"EventGhostについて..."
        AddAction = u"アクションを追加"
        AddEvent = u"イベントを追加"
        AddFolder = u"フォルダを追加"
        AddMacro = u"マクロを追加"
        AddPlugin = u"プラグインを追加"
        Apply = u"適用"
        CheckUpdate = u"ソフトウェアの更新を確認..."
        ClearLog = u"ログをクリア"
        Close = u"閉じる"
        CollapseAll = u"すべて折りたたむ"
        ConfigurationMenu = u"設定"
        Configure = u"アイテムを設定"
        Copy = u"コピー"
        Cut = u"切り取り"
        Delete = u"削除"
        Disabled = u"アイテムを無効"
        EditMenu = u"編集"
        Execute = u"アイテムを実行"
        Exit = u"終了"
        ExpandAll = u"すべて展開する"
        ExpandOnEvents = u"イベントが発生したら、自動的に展開しハイライト表示する"
        ExpandTillMacro = u"マクロだけ自動的にハイライト表示する"
        Export = u"エクスポート..."
        FileMenu = u"ファイル"
        Find = u"検索"
        FindNext = u"次を検索"
        HelpMenu = u"ヘルプ"
        HideShowToolbar = u"ツールバー"
        Import = u"インポート..."
        LogActions = u"アクションをログ表示"
        LogMacros = u"マクロをログ表示"
        LogTime = u"時間をログ表示"
        New = u"新規作成"
        Open = u"開く..."
        Options = u"オプション..."
        Paste = u"貼り付け"
        Redo = u"やり直し"
        Rename = u"アイテムを名称変更"
        Reset = u"リセット"
        Save = u"保存する"
        SaveAs = u"名前を付けて保存..."
        SelectAll = u"すべて選択"
        Undo = u"元に戻す"
        ViewMenu = u"表示"
        WebForum = u"サポート掲示板"
        WebHomepage = u"ホームページ"
        WebWiki = u"Wiki"
    class SaveChanges:
        mesg = u"ファイルの内容が変更されています。\n\n変更を保存しますか？"
        title = u"変更を保存しますか？"
    class TaskBarMenu:
        Exit = u"終了"
        Hide = u"最小化"
        Show = u"EventGhostを開く"
    class Tree:
        caption = u"設定"
class Error:
    FileNotFound = u'ファイル"%s"が見つかりません。'
    InAction = u'アクション・エラー: "%s"'
    configureError = u"設定エラー: %s"
    pluginLoadError = u"プラグイン・ファイル%sのローディング・エラー"
    pluginNotActivated = u'プラグイン"%s"が有効ではありません。'
    pluginStartError = u"プラグイン開始エラー: %s"
class Exceptions:
    DeviceInitFailed = u"デバイスを初期化できません！"
    DeviceNotFound = u"デバイスが見つかりません！"
    DeviceNotReady = u"デバイスが準備できていません！"
    DriverNotFound = u"デバイスが見つかりません！"
    DriverNotOpen = u"ドライバを開けません！"
    InitFailed = u"初期化失敗！"
    PluginNotFound = u"プラグインが見つかりません！"
    ProgramNotFound = u"アプリケーションが見つかりません！"
    ProgramNotRunning = u"アプリケーションが実行されていません！"
    SerialOpenFailed = u"シリアル・ポートを開けません！"
class CheckUpdate:
    ManErrorMesg = u"EventGhostのホームページから情報を取得できませんでした。\n\n後でまた実行してください。"
    ManErrorTitle = u"更新確認中にエラーが発生しました"
    ManOkMesg = u"このEventGhostは最新バージョンです。"
    ManOkTitle = u"最新バージョンが利用できません"
    downloadButton = u"ダウンロード・ページを訪問する"
    newVersionMesg = u"新しいバージョンのEventGhostがリリースされました。\n\n　　　　現在のバージョン:    %s\n　　　　最新のバージョン:    %s\n\nいまダウンロード・ページを訪問しますか？"
    title = u"新しいバージョンのEventGhostを利用できます..."
    waitMesg = u"EventGhostが更新情報を検索している間お待ちください。"
class AddActionDialog:
    descriptionLabel = u"説明"
    title = u"追加するアクションを選択..."
class AddPluginDialog:
    author = u"作者:"
    descriptionBox = u"説明"
    externalPlugins = u"外部デバイス"
    noInfo = u"情報がありません。"
    noMultiload = u"このプラグインはマルチ・ローディングをサポートしていません。既に設定でこのプラグインのインスタンスがあります。"
    noMultiloadTitle = u"マルチ・ローディングができません。"
    otherPlugins = u"その他"
    programPlugins = u"プログラム制御"
    remotePlugins = u"リモコン"
    title = u"追加するプラグインを追加..."
    version = u"バージョン:"
class AddActionGroupDialog:
    caption = u"アクションを追加？"
    message = u"EventGhostはツリー設定で、このプラグインのすべてのアクションを一つのフォルダに追加できます。\nもしそうしたいなら、追加したい場所を選択して、OKボタンを押してください。\n\nそうでなければキャンセル・ボタンを押してください。"
class OptionsDialog:
    CheckUpdate = u"起動時に新しいバージョンをチェックする"
    HideOnClose = u"閉じた時、システム・トレイに転送する"
    HideOnStartup = u"起動時、最小化する"
    LanguageGroup = u"言語"
    StartGroup = u"開始"
    StartWithWindows = u"Windows起動時に実行する"
    Tab1 = u"一般"
    Title = u"オプション"
    UseAutoloadFile = u"自動的に設定ファイルをロードする"
    Warning = u"言語の変更はアプリケーションを再起動した後に反映されます。"
    confirmDelete = u"ツリーアイテムの削除を確認する"
    limitMemory1 = u"最小化時、メモリ消費を制限する容量"
    limitMemory2 = u"MB"
class FindDialog:
    caseSensitive = u"大文字と小文字を区別する"
    direction = u"方向"
    down = u"下へ"
    findButton = u"次を検索"
    notFoundMesg = u'"%s"が見つかりません。'
    searchLabel = u"検索する文字列:"
    searchParameters = u"アクション変数を検索に含める"
    title = u"検索"
    up = u"上へ"
    wholeWordsOnly = u"完全一致のみ"
class AboutDialog:
    Author = u"作者: %s"
    CreationDate = u"%Y/%b/%d(%a) %H:%M:%S"
    Title = u"EventGhostについて"
    Version = u"バージョン: %s (ビルド %s)"
    tabAbout = u"EventGhostについて"
    tabChangelog = u"変更履歴"
    tabLicense = u"使用許諾契約"
    tabSpecialThanks = u"謝辞"
    tabSystemInfo = u"システム情報"
class Plugin:
    class EventGhost:
        name = u"EventGhost(JA)"
        description = u"EventGhostのコアとなる機能を制御するアクションです。"
        class AutoRepeat:
            name = u"マクロを自動繰り返し"
            description = u"マクロを自動繰り返しする。"
            seconds = u"秒"
            text1 = u"最初の繰り返しを始めるまでの時間"
            text2 = u"１回の繰り返し間隔"
            text3 = u"次の繰り返しを始めるまでの時間"
            text4 = u"１回の繰り返し間隔"
        class Comment:
            name = u"コメント"
            description = u"設定にコメントを付ける為のアクションで何もしない。"
        class DisableItem:
            name = u"アイテムを無効"
            description = u"アイテムを無効にする。"
            label = u"無効: %s"
            text1 = u"無効にしたいアイテムを選択してください:"
        class EnableExclusive:
            name = u"フォルダ／マクロを単独有効"
            description = u"設定で指定したフォルダ／マクロを有効にする。しかし同じ階層にある他のフォルダ／マクロは無効になります。"
            label = u"単独有効: %s"
            text1 = u"有効にしたいフォルダ／マクロを選択してください。"
        class EnableItem:
            name = u"アイテムを有効"
            description = u"アイテムを有効にする。"
            label = u"有効: %s"
            text1 = u"有効にしたいアイテムを選択してください:"
        class FlushEvents:
            name = u"保留イベントを破棄"
            description = u'キューイングされているイベントで、保留中のものを破棄します。\n\n<p><b>例:</b>\nリモコン・ボタンで制御する処理時間が長いマクロがある。そのイベント処理中、何度も続けてボタンを押してキューイングされた分について、マクロの最後に"保留イベントを破棄"を置くことで、すべての待ち処理を破棄することができる。'
        class JumpIf:
            name = u"条件ジャンプ"
            description = u"もしPython評価が真なら、他のマクロにジャンプする。"
            label1 = u"もし%sなら、%sにジャンプする"
            label2 = u"もし%sなら、関数%sにジャンプする"
            mesg1 = u"マクロを選択する..."
            mesg2 = u"条件が真のとき、実行するマクロを選択してください。"
            text1 = u"条件:"
            text2 = u"ジャンプ先:"
            text3 = u"実行した後に戻る"
        class JumpIfLongPress:
            name = u"ボタン長押しジャンプ"
            description = u"リモコン・ボタンを押している時間が設定時間より長ければ、他のマクロにジャンプする。"
            label = u"ボタンを%s秒押し続けたら、%sにジャンプする"
            text1 = u"ボタンを押している時間が"
            text2 = u"秒より長い場合の"
            text3 = u"ジャンプ先:"
            text4 = u"マクロを選択..."
            text5 = u"トリガとなるマクロを選択してください。"
        class NewJumpIf:
            name = u"ジャンプ"
            description = u"指定条件を満たせば、他のマクロにジャンプする。"
            choices = [
                u"最後のアクションが成功",
                u"最後のアクションが不成功",
                u"常時",
            ]
            labels = [
                u'もし成功なら、"%s"にジャンプする',
                u'もし不成功なら、"%s"にジャンプする',
                u'"%s"にジャンプする',
                u'もし成功なら、"%s"にジャンプして戻る',
                u'もし不成功なら、"%s"にジャンプして戻る',
                u'"%s"にジャンプして戻る',
            ]
            mesg1 = u"マクロを選択する..."
            mesg2 = u"条件を満たしたとき、実行するマクロを選択してください。"
            text1 = u"条件:"
            text2 = u"ジャンプ先:"
            text3 = u"実行した後に戻る"
        class PythonCommand:
            name = u"Pythonコマンド"
            description = u"Pythonの１行コードを実行する。"
            parameterDescription = u"Pythonコード:"
        class PythonScript:
            name = u"Pythonスクリプト"
            description = u"Pythonスクリプトを実行する。"
        class ShowOSD:
            name = u"オン・スクリーン・ディスプレイを表示"
            description = u"オン・スクリーン・ディスプレイを表示する。"
            alignment = u"配置:"
            alignmentChoices = [
                u"左上",
                u"右上",
                u"左下",
                u"右下",
                u"画面中央",
                u"下中央",
                u"上中央",
                u"左中央",
                u"右中央",
            ]
            display = u"ディスプレイ:"
            editText = u"表示する文字:"
            label = u"オン・スクリーン・ディスプレイを表示: %s"
            osdColour = u"文字色:"
            osdFont = u"文字フォント:"
            outlineFont = u"アウトライン・フォントを使う"
            skin = u"スキンを使う"
            wait1 = u" "
            wait2 = u"秒後(0 = 隠さない)にオン・スクリーン・ディスプレイを自動的に隠す"
            xOffset = u"X軸オフセット:"
            yOffset = u"Y軸オフセット:"
        class StopIf:
            name = u"条件停止"
            description = u"指定したPython評価が真なら、実行中のマクロを停止する。"
            label = u"もし%sなら、停止する"
            parameterDescription = u"Python条件:"
        class StopProcessing:
            name = u"イベント処理を停止"
            description = u"イベント処理を停止する。"
        class TriggerEvent:
            name = u"トリガ・イベント"
            description = u"イベントを発生させる原因(オプションで時間指定できる)"
            labelWithTime = u'%.2f秒後のトリガ・イベント"%s"'
            labelWithoutTime = u'トリガ・イベント"%s"'
            text1 = u"トリガになるイベント文字列:"
            text2 = u"トリガになるイベントの遅延時間:"
            text3 = u"秒(0=すぐトリガになる)"
        class Wait:
            name = u"待ち時間"
            description = u"一定時間待つ"
            label = u"待ち時間: %s秒"
            seconds = u"秒"
            wait = u"待ち時間"
    class System:
        name = u"System(JA)"
        description = u"サウンド・カード、グラフィック・カード、電源管理等のシステム・デバイスを制御する。"
        forced = u"強制終了: %s"
        forcedCB = u"すべてのプログラムを強制終了する"
        class ChangeDisplaySettings:
            name = u"ディスプレイ設定を変更"
            description = u"ディスプレイ設定を変更"
            colourDepth = u"色の深さ:"
            display = u"ディスプレイ:"
            frequency = u"周波数:"
            includeAll = u"モニタがサポートしていないモードを含む。"
            label = u"ディスプレイ%dをモード%dx%d@%d Hzに設定する"
            resolution = u"解像度:"
            storeInRegistry = u"レジストリにモードを保存する。"
        class ChangeMasterVolumeBy:
            name = u"マスタ音量を変更"
            description = u"現在の音量に対して、相対的にマスタ音量を変更する。"
            text1 = u"マスタ音量を"
            text2 = u"パーセント変更する。"
        class Execute:
            name = u"アプリケーション開始"
            description = u"実行ファイルを開始する。"
            FilePath = u"実行ファイル・パス:"
            Parameters = u"コマンド・ライン・オプション:"
            ProcessOptions = (
                u"リアルタイム",
                u"普通より上",
                u"普通",
                u"普通より下",
                u"アイドル",
            )
            ProcessOptionsDesc = u"プロセスの優先度:"
            WaitCheckbox = u"アプリケーションが終了するまで待つ。"
            WindowOptions = (
                u"普通",
                u"最小化",
                u"最大化",
                u"隠す",
            )
            WindowOptionsDesc = u"Windowsオプション:"
            WorkingDir = u"作業ディレクトリ:"
            browseExecutableDialogTitle = u"実行ファイルを選択する"
            browseWorkingDirDialogTitle = u"作業ディレクトリを選択する"
            label = u"プログラムを実行: %s"
        class Hibernate:
            name = u"パソコンを休止"
            description = u"ハードディスク上に現在の状態を記録し、電源供給を休止します。"
        class LockWorkstation:
            name = u"パソコンをロック"
            description = u"パソコンのディスプレイをロックします。パソコンをロックすることで不正利用を防ぐことができます。"
        class LogOff:
            name = u"ユーザをログオフ"
            description = u"現在のログオン・セッションで実行しているすべてのプロセスを終了し、ログオフします。"
        class MonitorGroup:
            name = u"ディスプレイ"
            description = u"ディスプレイの電源状態を制御します。"
        class MonitorPowerOff:
            name = u"モニタを電源オフ"
            description = u"モニタを電源オフの状態にします。消費電力を一番節約できるモードです。"
        class MonitorPowerOn:
            name = u"モニタを電源オン"
            description = u"省電力モードまたは電源オフの時、モニタの電源を投入します。またスクリーン・セーバを停止します。"
        class MonitorStandby:
            name = u"モニタをスタンバイ・モード"
            description = u"モニタを省電力モードの状態にします。"
        class MuteOff:
            name = u"ミュート・オフ"
            description = u"ミュートをオフする"
        class MuteOn:
            name = u"ミュート・オン"
            description = u"ミュートをオンする"
        class OpenDriveTray:
            name = u"ドライブ・トレイを開閉"
            description = u"CD/DVD-ROMドライブのトレイを制御する。"
            driveLabel = u"ドライブ:"
            labels = [
                u"ドライブ・トレイを切り替える: %s",
                u"ドライブ・トレイを取り出す: %s",
                u"ドライブ・トレイを閉じる: %s",
            ]
            options = [
                u"ドライブ・トレイの開閉を切り替える",
                u"ドライブ・トレイを開くだけ",
                u"ドライブ・トレイを閉じるだけ",
            ]
            optionsLabel = u"動作を選択"
        class PlaySound:
            name = u"音声を再生"
            description = u"音声を再生する"
            fileMask = u"Wavファイル (*.WAV)|*.wav|すべてのファイル (*.*)|*.*"
            text1 = u"音声ファイルのパス:"
            text2 = u"終了するまで待つ"
        class PowerDown:
            name = u"パソコンを電源切断"
            description = u"システムをシャット・ダウンし電源切断をします。システムで電源オフ仕様をサポートしていなければいけません。"
        class PowerGroup:
            name = u"電源管理"
            description = u"パソコンの停止・休止・再起動・電源切断をします。またパソコンをロックしたり、現在のユーザからログオフすることもできます。"
        class Reboot:
            name = u"パソコンを再起動"
            description = u"システムを終了し、再立ち上げします。"
        class RegistryChange:
            name = u"レジストリ値を変更"
            description = u"Windowsのレジストリ値を変更する"
            actions = (
                u"新規作成または変更",
                u"存在する場合のみ変更",
                u"削除",
            )
            labels = (
                u'"%s"を%sに変更',
                u'存在する場合のみ、"%s"を%sに変更',
                u'"%s"を削除',
            )
        class RegistryGroup:
            name = u"レジストリ"
            description = u"Windowsレジストリの値を問い合わせまたは変更する。"
            actionText = u"操作:"
            chooseText = u"レジストリ・キーを選択:"
            defaultText = u"(デフォルト)"
            keyOpenError = u"レジストリ・キーのオープン・エラー"
            keyText = u"キー:"
            keyText2 = u"キー"
            newValue = u"新しい値:"
            noKeyError = u"キーが指定されていません"
            noNewValueError = u"新しい値が指定されていません"
            noSubkeyError = u"サブ・キーが指定されていません"
            noTypeError = u"データ型が指定されていません"
            noValueNameError = u"キー名が指定されていません"
            noValueText = u"値が見つかりません"
            oldType = u"現在のデータ型:"
            oldValue = u"現在の値:"
            typeText = u"データ型:"
            valueChangeError = u"値を変更中にエラー"
            valueName = u"キー名:"
            valueText = u"値:"
        class RegistryQuery:
            name = u"レジストリの問い合わせ"
            description = u"Windowsのレジストリを検索し、値を返すか比較する。"
            actions = (
                u"存在するか確認する",
                u"結果を返す",
                u"比較する",
            )
            labels = (
                u'"%s"が存在するか確認する',
                u'結果として"%s"を返す',
                u'"%s"と%sを比較する',
            )
        class ResetIdleTimer:
            name = u"アイドル・タイマをリセット"
            description = u"アイドル・タイマをリセット"
        class SetClipboard:
            name = u"クリップボードにコピー"
            description = u"文字をシステムのクリップ・ボードにコピーする。"
            error = u"クリップ・ボードを開けません"
        class SetDisplayPreset:
            name = u"ディスプレイ・プリセットを設定"
            description = u"ディスプレイ・プリセットを設定"
            fields = (
                u"デバイス",
                u"左",
                u"上",
                u"幅",
                u"高さ",
                u"周波数",
                u"色の深さ",
                u"付属",
                u"最初",
                u"フラグ",
            )
            query = u"現在のディスプレイ設定を問い合わせする"
        class SetIdleTime:
            name = u"アイドル・タイムを設定"
            description = u"アイドル・タイムを設定"
            label1 = u"アイドル・イベントが切り替わる前に"
            label2 = u"秒待つ"
        class SetMasterVolume:
            name = u"マスタ音量を設定"
            description = u"マスタ音量を絶対値に設定する"
            text1 = u"マスタ音量を"
            text2 = u"パーセントに設定する。"
        class SetSystemIdleTimer:
            name = u"アイドル・タイマを設定"
            description = u"システムのアイドル・タイマを設定"
            choices = [
                u"システムのアイドル・タイマを無効",
                u"システムのアイドル・タイマを有効",
            ]
            text = u"オプション選択:"
        class SetWallpaper:
            name = u"壁紙を変更"
            description = u"壁紙を変更"
            choices = (
                u"中央に表示",
                u"並べて表示",
                u"拡大して表示",
            )
            fileMask = u"すべての画像ファイル|*.jpg;*.bmp;*.gif;*.png|すべてのファイル (*.*)|*.*"
            text1 = u"画像ファイル・パス:"
            text2 = u"整列:"
        class ShowPicture:
            name = u"画像を表示"
            description = u"画面に画像を表示します。"
            allFiles = u"すべてのファイル"
            allImageFiles = u"すべてのイメージ・ファイル"
            display = u"モニタ"
            path = u"画像のファイル・パス(クリアする場合は空にする):"
        class SoundGroup:
            name = u"サウンド・カード"
            description = u"サウンド・カードを制御するアクションです。"
        class Standby:
            name = u"パソコンを停止"
            description = u"メモリー上に現在の状態を保存し、電源供給を停止します。"
        class StartScreenSaver:
            name = u"スクリーン・セーバを開始"
            description = u"現在Windowsで選択されているスクリーン・セーバを開始する。"
        class ToggleMute:
            name = u"ミュートを切り替え"
            description = u"ミュートを切り替え"
        class WakeOnLan:
            name = u"Wake on LAN"
            description = u"特別なネットワーク・パケットを送り、他のパソコンを立ち上げる。"
            parameterDescription = u"立ち上げるパソコンのMACアドレス:"
    class Window:
        name = u"Window(JA)"
        description = u"特定のウィンドウを検索、移動、サイズ変更、キー入力といった、デスクトップ上のウィンドウ制御に関連したアクション。"
        class BringToFront:
            name = u"前面"
            description = u"特定のウィンドウを前面に出す。"
        class Close:
            name = u"閉じる"
            description = u"アプリケーション・ウィンドウを閉じる"
        class FindWindow:
            name = u"ウィンドウ検索"
            description = u'マクロでウィンドウのアクションを行う際に、その対象となるウィンドウを検索します。\n\n<p>マクロで"ウィンドウ検索"のアクションがなければ、すべてのウィンドウのアクションは、最前面のウィンドウが対象になります。\n<p>編集ボックスではワイルド・カードを使えます。{*}は任意の文字列、{?}は任意の一文字を意味します。'
            drag1 = u"私をウィンドウにドラックしてください。"
            drag2 = u"今から私をウィンドウに移動してください。"
            hide_box = u"ドラッグ中EventGhostを隠す"
            invisible_box = u"目に見えないウィンドウも検索"
            label = u"ウィンドウを検索: %s"
            label2 = u"最前面のウィンドウを検索"
            matchNum1 = u"値を返すのみ"
            matchNum2 = u"番目に一致"
            onlyFrontmost = u"最前面のウィンドウのみ一致"
            options = (
                u"プログラム:",
                u"ウィンドウ名:",
                u"ウィンドウ・クラス:",
                u"子ウィンドウ名:",
                u"子ウィンドウ・クラス:",
            )
            refresh_btn = u"更新"
            stopMacro = [
                u"ターゲットが見つからなければマクロを停止",
                u"ターゲットが見つかればマクロを停止",
                u"マクロを停止しない",
            ]
            testButton = u"テスト"
            wait1 = u"ウィンドウが表示されるまでの最大待ち時間"
            wait2 = u"秒"
        class Maximize:
            name = u"最大化"
            description = u"最大化"
        class Minimize:
            name = u"最小化"
            description = u"最小化"
        class MoveTo:
            name = u"絶対移動"
            description = u"絶対移動"
            label = u"ウィンドウを%sに移動"
            text1 = u"X座標を"
            text2 = u"ピクセルに設定する"
            text3 = u"Y座標を"
            text4 = u"ピクセルに設定する"
        class Resize:
            name = u"サイズ変更"
            description = u"ウィンドウをサイズ変更する"
            label = u"ウィンドウを%s, %sにサイズ変更する"
            text1 = u"幅を"
            text2 = u"ピクセルに設定する"
            text3 = u"高さを"
            text4 = u"ピクセルに設定する"
        class Restore:
            name = u"元に戻す"
            description = u"元に戻す"
        class SendKeys:
            name = u"キー入力をエミュレーション"
            description = u'このアクションは他のプログラムを制御するためのキー入力をエミュレーションします。\n編集ボックスにキー入力させたい文字をタイプするだけです。\n\n<p>\n特殊キーをエミュレーションするには、{}でキーワードを囲む必要があります。\n例えば、カーソルの↑の場合、<b>{Up}</b>と記入します。\n複数のキーを組み合わせて入力する場合は、+で連結させます。\n例えば<b>{Shift+Ctrl+F1}</b>や<b>{Ctrl+V}</b>のようになります。\nキーワードは大文字小文字の区別はないので、{SHIFT+ctrl+F1}と書くことも\nできます。\n<p>\nキーボードの左側と右側に配置されている同じキーは、"L"か"R"を先頭につけて\n区別することができます。<br><br>\n\nWindowsキー:<br>\n<b>{Win}</b> または <b>{LWin}</b> または <b>{RWin}</b>\n<p>\n他にEventGhostが理解できるキーワード一覧は下記です。<br>\n<b>{Ctrl}</b> または <b>{Control}<br>\n{Shift}<br>\n{Alt}<br>\n{Return}</b> または <b>{Enter}<br>\n{Back}</b> または <b>{Backspace}<br>\n{Tab}</b> または <b>{Tabulator}<br>\n{Esc}</b> または <b>{Escape}<br>\n{Spc}</b> または <b>{Space}<br>\n{Up}<br>\n{Down}<br>\n{Left}<br>\n{Right}<br>\n{PgUp}</b> または <b>{PageUp}<br>\n{PgDown}</b> または <b>{PageDown}<br>\n{Home}<br>\n{End}<br>\n{Ins}</b> または <b>{Insert}<br>\n{Del}</b> または <b>{Delete}<br>\n{Pause}<br>{Capslock}<br>\n{Numlock}<br>\n{Scrolllock}<br>\n{F1}, {F2}, ... , {F24}<br>\n{Apps}</b> (コンテキスト・メニュ・キー)<b><br>\n<br>\n</b>テンキーのエミュレーションは下記です:<b><br>\n{Divide}<br>\n{Multiply}<br>\n{Subtract}<br>\n{Add}<br>\n{Decimal}<br>\n{Numpad0}, {Numpad1}, ... , {Numpad9}</b>\n\n'
            insertButton = u"挿入"
            specialKeyTool = u"キー・ツール"
            textToType = u"入力文字:"
            useAlternativeMethod = u"代替方法でキー入力のエミュレーションをする"
            class Keys:
                backspace = u"Backspace"
                context = u"コンテキスト・メニュ・キー"
                delete = u"Delete"
                down = u"↓"
                end = u"End"
                enter = u"Enter"
                escape = u"Esc"
                home = u"Home"
                insert = u"Insert"
                left = u"←"
                num0 = u"Num 0"
                num1 = u"Num 1"
                num2 = u"Num 2"
                num3 = u"Num 3"
                num4 = u"Num 4"
                num5 = u"Num 5"
                num6 = u"Num 6"
                num7 = u"Num 7"
                num8 = u"Num 8"
                num9 = u"Num 9"
                numAdd = u"Num +"
                numDecimal = u"Num ."
                numDivide = u"Num /"
                numMultiply = u"Num *"
                numSubtract = u"Num -"
                pageDown = u"Page Down"
                pageUp = u"Page Up"
                returnKey = u"Enter"
                right = u"→"
                space = u"Space"
                tabulator = u"Tab"
                up = u"↑"
                win = u"Windowキー"
        class SendMessage:
            name = u"メッセージ送信"
            description = u"Windows-API SendMessage関数を使って、ウィンドウに特定のメッセージを送信します。もし望めばPostMessage関数も使えます。"
            text1 = u"SendMessage関数の代わりにPostMessage関数を使う"
        class SetAlwaysOnTop:
            name = u"最前面"
            description = u"最前面に置く"
            actions = (
                u"「常に最前面」をクリアする",
                u"「常に最前面」をセットする",
                u"「常に最前面」を切り替える",
            )
            radioBox = u"動作を選択:"
    class Mouse:
        name = u"Mouse(JA)"
        description = u"マウスを制御するアクションを提供する。"
        class GoDirection:
            name = u"マウスの方向移動開始"
            description = u"マウスの方向移動開始"
            label = u"マウスを%.2f°の方向に移動開始する"
            text1 = u"マウスを"
            text2 = u"の方向(0-360)に移動開始する"
        class LeftButton:
            name = u"マウス左ボタン"
            description = u"マウス左ボタン"
        class LeftDoubleClick:
            name = u"マウス左ボタンをダブル・クリック"
            description = u"マウス左ボタンをダブル・クリック"
        class MiddleButton:
            name = u"マウス中ボタン"
            description = u"マウス中ボタン"
        class MouseWheel:
            name = u"マウス・ホイールを回す"
            description = u"マウス・ホイールを回す"
            label = u"マウス・ホイールを%dクリック回す"
            text1 = u"マウス・ホイールを"
            text2 = u"クリック回す。(マイナスなら下方向に回す)"
        class MoveAbsolute:
            name = u"絶対移動"
            description = u"絶対移動"
            label = u"マウス座標をx:%s, y:%sに移動"
            text1 = u"X座標を"
            text2 = u"ピクセルに設定"
            text3 = u"Y座標を"
            text4 = u"ピクセルに設定"
        class MoveRelative:
            name = u"相対移動"
            description = u"相対移動"
            label = u"マウス座標をx:%s, y:% sに変更"
            text1 = u"X座標を"
            text2 = u"ピクセル変更"
            text3 = u"Y座標を"
            text4 = u"ピクセル変更"
        class RightButton:
            name = u"マウス右ボタン"
            description = u"マウス右ボタン"
        class RightDoubleClick:
            name = u"マウス右ボタンをダブル・クリック"
            description = u"マウス右ボタンをダブル・クリック"
        class ToggleLeftButton:
            name = u"マウス左ボタンを切り替え"
            description = u"マウス左ボタンを切り替え"
    class Joystick:
        name = u"Joystick"
    class Speech:
        name = u"Speech(JA)"
        description = u"Microsoft Speech API (SAPI)のText-To-Speechサービスを利用する。"
        class TextToSpeech:
            name = u"Text to speech"
            description = u"Microsoft Speech API (SAPI) を使い、文章をしゃべる。"
            buttonInsertDate = u"日付挿入"
            buttonInsertTime = u"時間挿入"
            errorCreate = u"ボイス・オブジェクトを生成できません"
            errorNoVoice = u"音声ファイル%sが利用できません"
            fast = u"速い"
            label = u"話す: %s"
            labelRate = u"速度:"
            labelVoice = u"音声:"
            labelVolume = u"音量:"
            loud = u"大声"
            normal = u"普通"
            silent = u"小声"
            slow = u"遅い"
            textBoxLabel = u"文字"
            voiceProperties = u"声の特性"
    class USB_UIRT:
        name = u"USB-UIRT(JA)"
        description = u'<a href="http://www.usbuirt.com/">USB-UIRT</a> トランシーバのハードウェア・プラグイン。\n\n<p><a href="http://www.usbuirt.com/"><p><center><img src="picture.jpg" alt="USB-UIRT" /></a></center>'
        blinkRx = u"IRを受信した時に点滅する"
        blinkTx = u"IRを送信した時に点滅する"
        irReception = u"IRの受付"
        legacyCodes = u"レガシUIRT2互換イベントを生成する"
        notFound = u"<見つかりません>"
        redIndicator = u"赤色LEDの動作"
        stopCodes = u"同じコードが続く場合、そのコードを一度だけ送信し、その後「繰り返し」を表す特殊コードを送信する"
        uuFirmDate = u"ファームウェアの日付:"
        uuFirmVersion = u"ファームウェアのバージョン:"
        uuInfo = u"USB-UIRT情報"
        uuProtocol = u"プロトコル・バージョン:"
        class TransmitIR:
            name = u"IR送信"
            description = u"USB-UIRTハードウェアを介してIRコードを送信する。"
            infinite = u"無限"
            irCode = u"IRコード:"
            learnButton = u"IRコードを学習する..."
            repeatCount = u"繰り返し数:"
            wait1 = u"待機時間:"
            wait2 = u"ms (IR送信前の待ち時間)"
            zone = u"ゾーン:"
            zoneChoices = (
                u"すべて",
                u"外付け右ピンジャック",
                u"外付け左ピンジャック",
                u"内蔵エミッタ",
            )
            class LearnDialog:
                acceptBurstButton = u"バーストを受け入れる"
                forceRaw = u"RAWモードで学習する"
                frequency = u"周波数"
                helpText = u"1. リモコンをUSB-UIRT正面に照準を定める。約15cm距離を置く。\n\n2. 学習が終わるまで、リモコンの学習させたいボタンを押し続ける..."
                progress = u"学習の進捗状況"
                signalQuality = u"信号"
                title = u"IRコードを学習する"
    class Webserver:
        name = u"Webserver(JA)"
        description = u"小さなWebサーバを実行します。HTMLページを介し、イベントを発生させて使います。"
        authBox = u"ベーシック認証"
        authPassword = u"パスワード:"
        authRealm = u"レルム:"
        authUsername = u"ユーザ名:"
        documentRoot = u"HTMLドキュメント・ルート:"
        eventPrefix = u"イベント・プレフィックス"
        generalBox = u"一般設定"
        port = u"TCP/IP ポート:"
    class Winamp:
        name = u"WinAmp(JA)"
        description = u'<a href="http://www.winamp.com/">Winamp</a> を制御するアクションを追加する。'
        infoGroupDescription = u"Winampの様々な情報を問い合わせするためのアクションです。これを用いると、例えば小さなLCD/VFDにWinampの情報を表示させることができます。"
        infoGroupName = u"情報検索"
        class ChangeRepeatStatus:
            name = u"繰り返しの状態を変更"
            description = u"プレイ・リストの繰り返しの状態を変更する。"
            radioBoxLabel = u"オプション"
            radioBoxOptions = [
                u"繰り返ししない",
                u"繰り返しする",
                u"繰り返しを切り替える",
            ]
        class ChangeShuffleStatus:
            name = u"シャッフルの状態を変更"
            description = u"シャッフルの状態を変更する。"
            radioBoxLabel = u"オプション"
            radioBoxOptions = [
                u"シャッフルしない",
                u"シャッフルする",
                u"シャッフルを切り替える",
            ]
        class ChangeVolume:
            name = u"音量レベルを変更"
            description = u"現在の音量に対して、相対的に音量を変更する。"
            label = u"音量を%.2f %%変更する"
            text1 = u"音量を"
            text2 = u"パーセント変更する。"
        class ChooseFile:
            name = u"ファイルを再生"
            description = u"ファイル・ダイアログを開く。"
        class DiscretePause:
            name = u"一時停止を区別"
            description = u"Winampが再生中なら一時停止するが、既に停止しているなら何もしない。"
        class ExVis:
            name = u"ビジュアライゼーションを実行"
            description = u"現在のビジュアライゼーション・プラグインを実行する。"
        class Exit:
            name = u"終了"
            description = u"Winampを終了する。"
        class Fadeout:
            name = u"フェード・アウト"
            description = u"フェード・アウトして停止する。"
        class FastForward:
            name = u"進む"
            description = u"5秒進む。"
        class FastRewind:
            name = u"戻る"
            description = u"5秒戻る。"
        class GetBitRate:
            name = u"ビット・レートを取得"
            description = u"現在演奏している曲のビット・レート(kbps)を取得する。"
        class GetChannels:
            name = u"チャンネル数を取得"
            description = u"現在演奏している曲のチャンネル数(モノラル、ステレオ)を取得する。"
        class GetDuration:
            name = u"演奏時間を取得"
            description = u"現在演奏している曲の演奏時間(秒)を取得する。"
        class GetElapsed:
            name = u"曲の経過時間を取得"
            description = u"現在演奏している曲の経過時間(秒)を取得する。"
        class GetLength:
            name = u"プレイ・リストの曲数を取得"
            description = u"プレイ・リストの曲数を取得する。"
        class GetPlayingSongTitle:
            name = u"現在演奏している曲のタイトルを取得"
            description = u"現在演奏している曲のタイトルを取得する。"
        class GetPosition:
            name = u"プレイ・リストの局番を取得"
            description = u"プレイ・リスト中で現在演奏している曲番(位置)を取得する。"
        class GetRepeatStatus:
            name = u"繰り返しの状態を取得"
            description = u"プレイ・リストの繰り返しの状態(1=リピート on, 0=リピート off)を取得する。"
        class GetSampleRate:
            name = u"サンプル・レートを取得"
            description = u"現在演奏している曲のサンプル・レート(khz)を取得する。"
        class GetShuffleStatus:
            name = u"シャッフルの状態を取得"
            description = u"シャッフルの状態(1=シャッフル on, 0=シャッフル off)を取得する。"
        class GetVolume:
            name = u"音量レベルを取得"
            description = u"音量レベルをパーセンテージ(%)で取得する。"
        class NextTrack:
            name = u"次のトラック"
            description = u"[次のトラック]ボタンを押す操作をシミュレーションする。"
        class Pause:
            name = u"一時停止"
            description = u"[一時停止]ボタンを押す操作をシミュレーションする。"
        class Play:
            name = u"再生"
            description = u"[再生]ボタンを押す操作をシミュレーションする。"
        class PreviousTrack:
            name = u"前のトラック"
            description = u"[前のトラック]ボタンを押す操作をシミュレーションする。"
        class SetVolume:
            name = u"音量レベルを設定"
            description = u"音量のパーセンテージ(%)を設定する。"
            label = u"音量を%.2f%%に設定する"
            text1 = u"音量を"
            text2 = u"パーセントに設定する。"
        class ShowFileinfo:
            name = u"ファイル情報を表示"
            description = u"情報ボックスを開く。"
        class Stop:
            name = u"停止"
            description = u"[停止]ボタンを押す操作をシミュレーションする。"
        class TogglePlay:
            name = u"再生を切り替え"
            description = u"Winampの再生と一時停止を切り替える。"
        class ToggleRepeat:
            name = u"繰り返しを切り替え"
            description = u"繰り返しを切り替える。"
        class ToggleShuffle:
            name = u"シャッフルを切り替え"
            description = u"シャッフルを切り替える。"
        class VolumeDown:
            name = u"音量を下げる"
            description = u"Winampの音量を1%小さくする。"
        class VolumeUp:
            name = u"音量を上げる"
            description = u"Winampの音量を1%大きくする。"
    class X10:
        name = u"X10 Remote(JA)"
        description = u'X10互換RFリモコンのハードウェア・プラグイン。\n\n<p>\nサポートしているリモコン:\n<ul>\n<li><a href="http://www.ati.com/products/remotewonder/index.html">\nATI Remote Wonder™</a></li>\n<li><a href="http://www.ati.com/products/remotewonderplus/index.html">\nATI Remote Wonder™ PLUS</a></li>\n<li><a href="http://www.snapstream.com/">\nSnapStream Firefly</a></li>\n<li><a href="http://www.nvidia.com/object/feature_PC_remote.html">\nNVIDIA Personal Cinema Remote</a></li>\n<li><a href="http://www.marmitek.com/">\nMarmitek PC Control</a></li>\n<li><a href="http://www.pearl.de/product.jsp?pdid=PE4444&catid=1601">\nPearl Q-Sonic Master Remote 6in1</a></li>\n<li><a href="http://www.niveusmedia.com/support/PCremote.htm">\nNiveus PC Remote Control</a></li>\n<li>Medion RF Remote Control</li>\n</ul>\n\n\n'
        allButton = u"すべて"
        errorMesg = u"X10レシーバが見つかりません！"
        idBox = u"アクティブIDs:"
        noneButton = u"なし"
        remoteBox = u"リモコンの種類:"
        usePrefix = u"イベント・プレフィックス:"
    class X10_CM15A:
        name = u"X10 CM15A(JA)"
        description = u'<a href="http://www.x10.com/activehomepro/sneakpreview.html">CM15A</a> トランシーバのハードウェア・プラグイン\n\n<p><a href="http://www.x10.com/activehomepro/sneakpreview.html"><p><center><img src="picture.jpg" alt="CM15A" /></a></center>'
        class TransmitX10:
            name = u"X10送信"
            description = u"ハードウェアCM15Aを介してX10コマンドを送信する。"
            cmdType = u"コマンド:"
            cmdTypeChoices = (
                u"PLC",
                u"RF",
            )
            houseCode = u"ハウス・コード:"
            percent = u"パーセント:"
            sendLabel = u"送信"
            state = u"状態:"
            stateChoices = (
                u"Off",
                u"On",
                u"Bright",
                u"Dim",
                u"All Lights Off",
                u"All Lights On",
            )
            unitCode = u"ユニット・コード:"
