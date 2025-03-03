# BlenderBIM Add-on - OpenBIM Blender Add-on
# Copyright (C) 2022 Dion Moult <dion@thinkmoult.com>
#
# This file is part of BlenderBIM Add-on.
#
# BlenderBIM Add-on is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BlenderBIM Add-on is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BlenderBIM Add-on.  If not, see <http://www.gnu.org/licenses/>.


import blenderbim.core.system as subject
from test.core.bootstrap import ifc, system


class TestLoadSystems:
    def test_run(self, system):
        system.import_systems().should_be_called()
        system.enable_system_editing_ui().should_be_called()
        system.disable_editing_system().should_be_called()
        subject.load_systems(system)


class TestDisableSystemEditingUI:
    def test_run(self, system):
        system.disable_editing_system().should_be_called()
        system.disable_system_editing_ui().should_be_called()
        subject.disable_system_editing_ui(system)


class TestAddSystem:
    def test_run(self, ifc, system):
        ifc.run("system.add_system", ifc_class="ifc_class").should_be_called()
        system.import_systems().should_be_called()
        subject.add_system(ifc, system, ifc_class="ifc_class")


class TestEditSystem:
    def test_run(self, ifc, system):
        system.export_system_attributes().should_be_called().will_return("attributes")
        ifc.run("system.edit_system", system="system", attributes="attributes").should_be_called()
        system.disable_editing_system().should_be_called()
        system.import_systems().should_be_called()
        subject.edit_system(ifc, system, system="system")


class TestRemoveSystem:
    def test_run(self, ifc, system):
        ifc.run("system.remove_system", system="system").should_be_called()
        system.import_systems().should_be_called()
        subject.remove_system(ifc, system, system="system")


class TestEnableEditingSystem:
    def test_run(self, system):
        system.import_system_attributes("system").should_be_called()
        system.set_active_system("system").should_be_called()
        subject.enable_editing_system(system, system="system")


class TestDisableEditingSystem:
    def test_run(self, system):
        system.disable_editing_system().should_be_called()
        subject.disable_editing_system(system)


class TestAssignSystem:
    def test_run(self, ifc):
        ifc.run("system.assign_system", product="product", system="system").should_be_called()
        subject.assign_system(ifc, system="system", product="product")


class TestUnassignSystem:
    def test_run(self, ifc):
        ifc.run("system.unassign_system", product="product", system="system").should_be_called()
        subject.unassign_system(ifc, system="system", product="product")


class TestSelectSystemProducts:
    def test_run(self, system):
        system.select_system_products("system").should_be_called()
        subject.select_system_products(system, system="system")


class TestShowPorts:
    def test_run(self, system):
        system.get_ports("element").should_be_called().will_return(["port"])
        system.load_ports(["port"]).should_be_called()
        system.select_elements(["port"]).should_be_called()
        subject.show_ports(system, element="element")


class TestHidePorts:
    def test_run(self, system):
        system.get_ports("element").should_be_called().will_return(["port"])
        system.delete_element_objects(["port"]).should_be_called()
        subject.hide_ports(system, element="element")


class TestAddPort:
    def test_run(self, ifc, system):
        system.get_ports("element").should_be_called().will_return(["port"])
        system.load_ports(["port"]).should_be_called()
        system.create_empty_at_cursor_with_element_orientation("element").should_be_called().will_return("obj")
        system.run_root_assign_class(obj="obj", ifc_class="IfcDistributionPort").should_be_called().will_return("port")
        ifc.run("system.assign_port", element="element", port="port").should_be_called()
        subject.add_port(ifc, system, element="element")


class TestSetFlowDirection:
    def test_run(self, ifc, system):
        system.get_connected_port("port").should_be_called().will_return("port2")
        ifc.run("system.connect_port", port1="port", port2="port2", direction="direction").should_be_called()
        subject.set_flow_direction(ifc, system, port="port", direction="direction")

    def test_do_not_set_a_direction_if_port_is_not_connected(self, ifc, system):
        system.get_connected_port("port").should_be_called().will_return(None)
        subject.set_flow_direction(ifc, system, port="port", direction="direction")
