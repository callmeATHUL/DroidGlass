import QtQuick
import Quickshell
import qs.Commons
import qs.Ui

BarWidget {
  id: root
  moduleName: "syntax_mind.phone"

  implicitWidth: button.implicitWidth
  implicitHeight: button.implicitHeight

  BarIconButton {
    id: button
    anchors.fill: parent
    bar: root.bar
    text: "\uf10b"
    slotSize: Style.bar.statusSlot
    fontSize: Style.font.caption
    tooltipText: "Phone mirror (show/hide)"
    onPressed: if (root.bar) root.bar.run("phone show")
  }
}
