import QtQuick
import Quickshell
import qs.Commons
import qs.Ui

BarWidget {
  id: root
  moduleName: "droidglass.mirror"

  // omarchy plugin add installs the repository at this stable user-owned path.
  // Calling the bundled CLI keeps the widget self-contained and does not start
  // the optional daemon or any phone/AI workflow on shell startup.
  readonly property string pluginRoot: (Quickshell.env("HOME") || "")
    + "/.config/omarchy/plugins/droidglass.mirror"

  implicitWidth: button.implicitWidth
  implicitHeight: button.implicitHeight

  // State tracking (0: Disconnected/Standby, 1: Mirrored/Screen Dark)
  property int mirrorState: 1

  BarIconButton {
    id: button
    anchors.fill: parent
    bar: root.bar
    text: root.mirrorState === 1 ? "\uf10b" : "\uf3cd"
    slotSize: Style.bar.statusSlot
    fontSize: Style.font.caption
    tooltipText: root.mirrorState === 1 
      ? "DroidGlass: Mirrored (Screen Dark)" 
      : "DroidGlass: Phone Active / Standby"
    onPressed: if (root.bar)
      root.bar.run(Util.shellQuote(root.pluginRoot + "/bin/droidglass") + " show")
  }
}
