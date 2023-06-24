# (C) 2023 Jerry Terra
# Use of this source code is governed by MIT license that can be found in the LICENSE file.

from kicad_sym import Pin, KicadSymbol, KicadLibrary


class CommonPin:
    def __init__(self, pin, etype, name):
        self.pin = pin
        self.name = name
        self.etype = etype


class Symbol:
    def __init__(self, name, lib):
        self.pin_set = []
        self.name = name
        self.lib = lib

    def add_pin(self, p: CommonPin):
        self.pin_set.append(p)

    def generate(self) -> KicadSymbol:
        ksym = KicadSymbol(self.name, self.lib.name, self.lib.name+".kicad_sym")

        ksym.add_default_properties()
        ksym.on_board = True
        ksym.in_bom = True

        y = 0.0

        for p in self.pin_set:
            etype = ""
            if p.etype == "<>":
                etype = "bidirectional"
            elif p.etype == "<-":
                etype = "input"
            elif p.etype == "->":
                etype = "output"
            elif p.etype == "--":
                etype = "passive"
            elif p.etype == "PI":
                etype = "power_in"
            elif p.etype == "PO":
                etype = "power_out"
            elif p.etype == "OC":
                etype = "open_collector"
            elif p.etype == "3S":
                etype = "tri_state"
            elif p.etype == "XX":
                etype = "no_connect"
            else:
                raise "Unknown etype"

            ksym.pins.append(Pin(number=p.pin, name=p.name, etype=etype, length=2.54, posy=y))

            y += 2.54

        return ksym


class Library:
    def __init__(self, name):
        self.name = name
        self.syms = []

    def add_sym(self, sym):
        self.syms.append(sym)

    def generate(self, filename: str):
        ksyms = []
        for sym in self.syms:
            ksyms.append(sym.generate())
        lib = KicadLibrary(filename, ksyms)
        lib.write()


def parse_pin_description(sym, filename: str):
    f = open(filename)

    while True:
        line = f.readline()
        s = line.split(" ")
        if len(s) != 3:
            break
        sym.add_pin(CommonPin(s[0], s[1], s[2]))
