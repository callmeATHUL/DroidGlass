import QtQuick
import Quickshell
import qs.Commons
import qs.Ui

BarWidget {
  id: root
  moduleName: "bq.ai.companion"

  implicitWidth: button.implicitWidth
  implicitHeight: button.implicitHeight

  BarIconButton {
    id: button
    anchors.fill: parent
    bar: root.bar
    text: "\uf1c0" // Database / Cloud icon
    slotSize: Style.bar.statusSlot
    fontSize: Style.font.caption
    tooltipText: "BigQuery AI: Click to evaluate clipboard SQL"
    onPressed: if (root.bar) root.bar.run("bq-ai-clip")
  }
}
