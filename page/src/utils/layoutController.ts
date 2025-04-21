type WindowCoords = {
  left: string;
  top: string;
  right: string;
  bottom: string;
}

export class LayoutController {
  visCoords: WindowCoords[] = chartViewports1;
  dialogCoords: WindowCoords = dialogCoords0;

  updateVisCoords(numberVis: number) {
    if (numberVis <= 1) {
      this.visCoords = chartViewports1;
    }
    else if (numberVis == 2) {
      this.visCoords = chartViewports2;
    }
    else if (numberVis > 2) {
      this.visCoords = chartViewports5;
    }
    else {
      this.visCoords = chartViewports5;
    }

    if (numberVis == 0) {
      this.dialogCoords = dialogCoords0;
    } else if (numberVis <= 3) {
      this.dialogCoords = dialogCoords3;
    } else if (numberVis <= 4) {
      this.dialogCoords = dialogCoords4;
    } else {
      this.dialogCoords = dialogCoords5;
    }
  }
}

const dialogCoords0 = {
  left: "10%",
  top: "10%",
  right: "10%",
  bottom: "0%",
}

const dialogCoords3 = {
  left: "10%",
  top: "70%",
  right: "10%",
  bottom: "0%",
}

const dialogCoords4 = {
  left: "30%",
  top: "70%",
  right: "10%",
  bottom: "0%",
}

const dialogCoords5 = {
  left: "30%",
  top: "70%",
  right: "30%",
  bottom: "0%",
}

const chartViewports1 = [
  { left: "20%", top: "5%", right: "20%", bottom: "35%" },
]

const vp2 = {
  pw: 5,
  ph: 10,
  g: 5,
}
const chartViewports2 = [
  { left: `${50 + vp2.g / 2}%`, top: `${vp2.ph}%`, right: `${vp2.pw}%`, bottom: `${vp2.ph + 30}%` },
  { left: `${vp2.pw}%`, top: `${vp2.ph}%`, right: `${50 + vp2.g / 2}%`, bottom: `${vp2.ph + 30}%` },
]

const vp3 = {
  pw: 2,
  ph: 5,
  gw: 2,
  gh: 5,
  pc: 30,
}

const chartViewports5 = [
  { left: `${vp3.pc}%`, top: `${vp3.ph}%`, right: `${vp3.pc}%`, bottom: `${vp3.ph + 30}%` },
  { left: `${vp3.pw}%`, top: `${vp3.ph}%`, right: `${100 - vp3.pc + vp3.gw}%`, bottom: `${50 + vp3.gh / 2}%` },
  { left: `${100 - vp3.pc + vp3.gw}%`, top: `${vp3.ph}%`, right: `${vp3.pw}%`, bottom: `${50 + vp3.gh / 2}%` },
  { left: `${vp3.pw}%`, top: `${50 + vp3.gh / 2}%`, right: `${100 - vp3.pc + vp3.gw}%`, bottom: `${vp3.ph}%` },
  { left: `${100 - vp3.pc + vp3.gw}%`, top: `${50 + vp3.gh / 2}%`, right: `${vp3.pw}%`, bottom: `${vp3.ph}%` },
]
