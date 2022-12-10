"""Tests for Tuya quirks."""

import datetime
from unittest import mock

import pytest
import zigpy.types as t
from zigpy.zcl import foundation

import zhaquirks
from zhaquirks.tuya import TUYA_GET_DATA, TUYA_MCU_VERSION_RSP, TUYA_SET_TIME
from zhaquirks.tuya.mcu import (
    ATTR_MCU_VERSION,
    TuyaAttributesCluster,
    TuyaClusterData,
    TuyaDPType,
    TuyaMCUCluster,
)

from tests.common import ClusterListener, MockDatetime

zhaquirks.setup()


# [zigpy.application] Received a packet: ZigbeePacket(src=AddrModeAddress(addr_mode=<AddrMode.NWK: 2>, address=0x6F8F), src_ep=1, dst=AddrModeAddress(addr_mode=<AddrMode.NWK: 2>, address=0x0000), dst_ep=1, source_route=None, extended_timeout=False, tsn=129, profile_id=260, cluster_id=61184, data=Serialized[b'\te\x01\x00G\x02\x02\x00\x04\x00\x00\x00\xfa'], tx_options=<TransmitOptions.NONE: 0>, radius=0, non_member_radius=0, lqi=255, rssi=-61)

# [zigpy.zcl] [0x6F8F:1:0xef00] Received ZCL frame: b'\te\x01\x00G\x02\x02\x00\x04\x00\x00\x00\xfa'
# [zigpy.zcl] [0x6F8F:1:0xef00] Decoded ZCL frame header: ZCLHeader(frame_control=FrameControl(frame_type=<FrameType.CLUSTER_COMMAND: 1>, is_manufacturer_specific=0, direction=<Direction.Client_to_Server: 1>, disable_default_response=0, reserved=0, *is_cluster=True, *is_general=False, *is_reply=True), tsn=101, command_id=1, *direction=<Direction.Client_to_Server: 1>, *is_reply=True)
# [zigpy.zcl] [0x6F8F:1:0xef00] Decoded ZCL frame: TuyaLevelControlManufCluster:get_data(data=TuyaCommand(status=0, tsn=71, datapoints=[TuyaDatapointData(dp=2, data=TuyaData(dp_type=<TuyaDPType.VALUE: 2>, function=0, raw=b'\xfa\x00\x00\x00', *payload=250))]))
# [zigpy.zcl] [0x6F8F:1:0xef00] Received command 0x01 (TSN 101): get_data(data=TuyaCommand(status=0, tsn=71, datapoints=[TuyaDatapointData(dp=2, data=TuyaData(dp_type=<TuyaDPType.VALUE: 2>, function=0, raw=b'\xfa\x00\x00\x00', *payload=250))]))
# [homeassistant.components.zha.core.channels.base] [0x6F8F:1:0x0008]: received attribute: 0 update with value: 63


# [zigpy.zcl] [0x6F8F:1:0x0008] Sending Tuya Cluster Command. Cluster Command is 4, Arguments are ()
# [zigpy.zcl] [0x6F8F:1:0xef00] tuya_mcu_command: cluster_data=TuyaClusterData(endpoint_id=1, cluster_attr='on_off', attr_value=True, expect_reply=True)
# [zigpy.zcl] [0x6F8F:1:0xef00] get_dp_mapping --> found DP: 1
# [zigpy.zcl] [0x6F8F:1:0xef00] from_cluster_data: 1, DPToAttributeMapping(ep_attribute='on_off', attribute_name='on_off', dp_type=<TuyaDPType.BOOL: 1>, converter=None, dp_converter=None, endpoint_id=None)
# [zigpy.zcl] [0x6F8F:1:0xef00] ztype: Bool.true
# [zigpy.zcl] [0x6F8F:1:0xef00] from_value: [1, 1]
# [zigpy.zcl] [0x6F8F:1:0xef00] raw: b'\x01'
# [zigpy.zcl] [0x6F8F:1:0xef00] tuya_command: TuyaCommand(status=0, tsn=96, datapoints=[TuyaDatapointData(dp=1, data=TuyaData(dp_type=<TuyaDPType.BOOL: 1>, function=0, raw=b'\x01', *payload=<Bool.true: 1>))])

# [zigpy.zcl] [0x6F8F:1:0xef00] tuya_mcu_command: cluster_data=TuyaClusterData(endpoint_id=1, cluster_attr='current_level', attr_value=166, expect_reply=True)
# [zigpy.zcl] [0x6F8F:1:0xef00] get_dp_mapping --> found DP: 2
# [zigpy.zcl] [0x6F8F:1:0xef00] from_cluster_data: 2, DPToAttributeMapping(ep_attribute='level', attribute_name='current_level', dp_type=<TuyaDPType.VALUE: 2>, converter=<function TuyaLevelControlManufCluster.<lambda> at 0x7f50d952e680>, dp_converter=<function TuyaLevelControlManufCluster.<lambda> at 0x7f50d952e710>, endpoint_id=None)
# [zigpy.zcl] [0x6F8F:1:0xef00] converted: 650
# [zigpy.zcl] [0x6F8F:1:0xef00] ztype: 650
# [zigpy.zcl] [0x6F8F:1:0xef00] from_value: [4, 0, 0, 2, 138]
# [zigpy.zcl] [0x6F8F:1:0xef00] raw: b'\x00\x00\x02\x8a'
# [zigpy.zcl] [0x6F8F:1:0xef00] tuya_command: TuyaCommand(status=0, tsn=97, datapoints=[TuyaDatapointData(dp=2, data=TuyaData(dp_type=<TuyaDPType.VALUE: 2>, function=0, raw=b'\x00\x00\x02\x8a', *payload=2315386880))])
# [homeassistant.components.zha.core.channels.base] [0x6F8F:1:0x0008]: executed 'move_to_level_with_on_off' command with args: '()' kwargs: '{'level': 166, 'transition_time': 0}' result: Default_Response(command_id=4, status=<Status.SUCCESS: 0>)
# [homeassistant.components.zha.entity] light.youssefs_room_level_on_off: starting transitioning timer for 0.25
# [homeassistant.components.zha.entity] light.youssefs_room_level_on_off: turned on: {'move_to_level_with_on_off': Default_Response(command_id=4, status=<Status.SUCCESS: 0>)}
# [zigpy.zcl] [0x6F8F:1:0xef00] Sending request header: ZCLHeader(frame_control=FrameControl(frame_type=<FrameType.CLUSTER_COMMAND: 1>, is_manufacturer_specific=True, direction=<Direction.Server_to_Client: 0>, disable_default_response=0, reserved=0, *is_cluster=True, *is_general=False, *is_reply=False), manufacturer=4098, tsn=98, command_id=0, *direction=<Direction.Server_to_Client: 0>, *is_reply=False)
# [zigpy.zcl] [0x6F8F:1:0xef00] Sending request: set_data(data=TuyaCommand(status=0, tsn=96, datapoints=[TuyaDatapointData(dp=1, data=TuyaData(dp_type=<TuyaDPType.BOOL: 1>, function=0, raw=b'\x01', *payload=<Bool.true: 1>))]))
# [zigpy.zcl] [0x6F8F:1:0xef00] Sending request header: ZCLHeader(frame_control=FrameControl(frame_type=<FrameType.CLUSTER_COMMAND: 1>, is_manufacturer_specific=True, direction=<Direction.Server_to_Client: 0>, disable_default_response=0, reserved=0, *is_cluster=True, *is_general=False, *is_reply=False), manufacturer=4098, tsn=100, command_id=0, *direction=<Direction.Server_to_Client: 0>, *is_reply=False)
# [zigpy.zcl] [0x6F8F:1:0xef00] Sending request: set_data(data=TuyaCommand(status=0, tsn=97, datapoints=[TuyaDatapointData(dp=2, data=TuyaData(dp_type=<TuyaDPType.VALUE: 2>, function=0, raw=b'\x00\x00\x02\x8a', *payload=2315386880))]))


@pytest.mark.parametrize(
    "quirk", (zhaquirks.tuya.ts0601_dimmer.TuyaSingleSwitchDimmer,)
)
@pytest.mark.parametrize(
    "zcl_frame, zcl_command, sequence, cluster_attr, dp, dp_type, raw, payload, attr_value",
    (
        (
            b'\t!\x01\x00E\x02\x02\x00\x04\x00\x03\x00\x00',
            TUYA_GET_DATA,
            69,
            "current_level",
            2, 
            TuyaDPType.VALUE, 
            b'\x00\x03\x00\x00', 
            196608,
            50135,
        ),
        (
            b'\te\x01\x00G\x02\x02\x00\x04\x00\x00\x00\xfa',
            TUYA_GET_DATA,
            71,
            "current_level",
            2, 
            TuyaDPType.VALUE, 
            b'\x00\x00\x00\xfa', 
            250,
            64,
        ),
    ),
)
async def test_dimming(zigpy_device_from_quirk, quirk, zcl_frame, zcl_command, sequence, cluster_attr, dp, dp_type, raw, payload, attr_value):
    """Test TuyaDPType.VALUE messages."""

    tuya_device = zigpy_device_from_quirk(quirk)

    tuya_cluster = tuya_device.endpoints[1].tuya_manufacturer
    cluster_listener = ClusterListener(tuya_cluster)

    assert len(cluster_listener.attribute_updates) == 0

    # simulate a TUYA_MCU_VERSION_RSP message
    hdr, args = tuya_cluster.deserialize(zcl_frame)
    assert hdr.command_id == zcl_command
    assert args
    assert args.data
    assert args.data.datapoints
    assert len(args.data.datapoints) == 1
    assert args.data.datapoints[0].dp == dp
    assert args.data.datapoints[0].data.dp_type == dp_type
    assert args.data.datapoints[0].data.raw == raw
    assert args.data.datapoints[0].data.payload == payload



    # p1 = mock.patch.object(motion_cluster, "reset_s", 0)
    # p2 = mock.patch.object(occupancy_cluster, "reset_s", 0)
    # with p1, p2:
    #     motion_cluster.handle_message(hdr, args)

    m1 = mock.patch.object(tuya_cluster.endpoint.device.application, "get_sequence", return_value=sequence)
    
    with m1:
        tcd = TuyaClusterData(
            endpoint_id=1, cluster_attr=cluster_attr, attr_value=attr_value, expect_reply=True
        )

        tuya_cmd = tuya_cluster.from_cluster_data(tcd)


        # assert not tuya_cmd
        assert tuya_cmd == args.data
        # assert not tuya_cmd.serialize()



ZCL_TUYA_VERSION_RSP = b"\x09\x06\x11\x01\x6D\x82"
ZCL_TUYA_SET_TIME = b"\x09\x12\x24\x0D\x00"


@pytest.mark.parametrize(
    "quirk", (zhaquirks.tuya.ts0601_dimmer.TuyaDoubleSwitchDimmer,)
)
async def test_tuya_version(zigpy_device_from_quirk, quirk):
    """Test TUYA_MCU_VERSION_RSP messages."""

    tuya_device = zigpy_device_from_quirk(quirk)

    tuya_cluster = tuya_device.endpoints[1].tuya_manufacturer
    cluster_listener = ClusterListener(tuya_cluster)

    assert len(cluster_listener.attribute_updates) == 0

    # simulate a TUYA_MCU_VERSION_RSP message
    hdr, args = tuya_cluster.deserialize(ZCL_TUYA_VERSION_RSP)
    assert hdr.command_id == TUYA_MCU_VERSION_RSP

    tuya_cluster.handle_message(hdr, args)
    assert len(cluster_listener.attribute_updates) == 1
    assert cluster_listener.attribute_updates[0][0] == ATTR_MCU_VERSION
    assert cluster_listener.attribute_updates[0][1] == "2.0.2"

    with mock.patch.object(tuya_cluster, "handle_mcu_version_response") as m1:
        tuya_cluster.handle_message(hdr, args)

        assert len(cluster_listener.cluster_commands) == 2
        assert cluster_listener.cluster_commands[1][1] == TUYA_MCU_VERSION_RSP
        assert cluster_listener.cluster_commands[1][2].version.version_raw == 130
        assert cluster_listener.cluster_commands[1][2].version.version == "2.0.2"

        m1.assert_called_once_with(
            tuya_cluster.MCUVersion(status=1, tsn=109, version_raw=130)
        )

    # read 'mcu_version' from cluster's attributes
    succ, fail = await tuya_cluster.read_attributes(("mcu_version",))
    assert succ["mcu_version"] == "2.0.2"


@pytest.mark.parametrize(
    "quirk", (zhaquirks.tuya.ts0601_dimmer.TuyaDoubleSwitchDimmer,)
)
async def test_tuya_mcu_set_time(zigpy_device_from_quirk, quirk):
    """Test set_time requests (0x24) messages for MCU devices."""

    tuya_device = zigpy_device_from_quirk(quirk)

    tuya_cluster = tuya_device.endpoints[1].tuya_manufacturer
    cluster_listener = ClusterListener(tuya_cluster)

    # Mock datetime
    origdatetime = datetime.datetime
    datetime.datetime = MockDatetime

    # simulate a SET_TIME message
    hdr, args = tuya_cluster.deserialize(ZCL_TUYA_SET_TIME)
    assert hdr.command_id == TUYA_SET_TIME

    with mock.patch.object(
        TuyaAttributesCluster, "command"
    ) as m1:  # tuya_cluster parent class (because of super() call)
        tuya_cluster.handle_message(hdr, args)

        assert len(cluster_listener.cluster_commands) == 1
        assert cluster_listener.cluster_commands[0][1] == TUYA_SET_TIME

        m1.assert_called_once_with(
            TUYA_SET_TIME, [0, 0, 28, 32, 0, 0, 14, 16], expect_reply=False
        )

    # restore datetime
    datetime.datetime = origdatetime  # restore datetime


@pytest.mark.parametrize(
    "quirk", (zhaquirks.tuya.ts0601_dimmer.TuyaDoubleSwitchDimmer,)
)
async def test_tuya_methods(zigpy_device_from_quirk, quirk):
    """Test TUYA_MCU_VERSION_RSP messages."""

    tuya_device = zigpy_device_from_quirk(quirk)

    tuya_cluster = tuya_device.endpoints[1].tuya_manufacturer
    dimmer2_cluster = tuya_device.endpoints[2].level
    switch1_cluster = tuya_device.endpoints[1].on_off

    tcd_1 = TuyaClusterData(endpoint_id=2, cluster_attr="minimum_level", attr_value=25)

    tcd_switch1_on = TuyaClusterData(
        endpoint_id=1, cluster_attr="on_off", attr_value=1, expect_reply=True
    )
    tcd_dimmer2_on = TuyaClusterData(
        endpoint_id=2, cluster_attr="on_off", attr_value=1, expect_reply=True
    )
    tcd_dimmer2_off = TuyaClusterData(
        endpoint_id=2, cluster_attr="on_off", attr_value=0, expect_reply=True
    )
    tcd_dimmer2_level = TuyaClusterData(
        endpoint_id=2, cluster_attr="current_level", attr_value=75, expect_reply=True
    )
    tcd_dimmer2_level0 = TuyaClusterData(
        endpoint_id=2, cluster_attr="current_level", attr_value=0, expect_reply=True
    )

    result_1 = tuya_cluster.from_cluster_data(tcd_1)
    assert result_1
    assert result_1.datapoints
    assert len(result_1.datapoints) == 1
    assert result_1.datapoints[0].dp == 9
    assert result_1.datapoints[0].data.dp_type == TuyaDPType.VALUE
    assert result_1.datapoints[0].data.raw == b"\x00\x00\x00b"

    tcd_2 = TuyaClusterData(
        endpoint_id=7, cluster_attr="not_exists_attribute", attr_value=25
    )
    result_2 = tuya_cluster.from_cluster_data(tcd_2)
    assert not result_2

    with mock.patch.object(tuya_cluster, "create_catching_task") as m1:
        tuya_cluster.tuya_mcu_command(tcd_2)
        # no DP resolution will not call TUYA_SET_DATA command
        m1.assert_not_called()

    result_3 = await dimmer2_cluster.command(0x0006)
    assert result_3.status == foundation.Status.UNSUP_CLUSTER_COMMAND

    with mock.patch.object(tuya_cluster, "tuya_mcu_command") as m1:
        rsp = await switch1_cluster.command(0x0001)

        m1.assert_called_once_with(tcd_switch1_on)
        assert rsp.status == foundation.Status.SUCCESS
        assert m1.call_count == 1

        rsp = await switch1_cluster.command(0x0004)
        m1.assert_called_once_with(tcd_switch1_on)  # no extra calls
        assert rsp.status == foundation.Status.UNSUP_CLUSTER_COMMAND
        assert m1.call_count == 1

        # test `move_to_level_with_on_off` quirk (call on_off + current_level)
        rsp = await dimmer2_cluster.command(0x0004, 75)
        assert rsp.status == foundation.Status.SUCCESS
        m1.assert_any_call(tcd_dimmer2_on)  # on_off
        m1.assert_called_with(tcd_dimmer2_level)  # current_level
        assert m1.call_count == 3

        # test `move_to_level_with_on_off` quirk (call on_off + current_level)
        rsp = await dimmer2_cluster.command(
            0x0004, 75, 0
        )  # extra args ¿transition time?. Not on_off for sure
        assert rsp.status == foundation.Status.SUCCESS
        m1.assert_any_call(tcd_dimmer2_on)  # on_off
        m1.assert_called_with(tcd_dimmer2_level)  # current_level
        assert m1.call_count == 5

        # test `move_to_level_with_on_off` quirk (call on_off + current_level)
        rsp = await dimmer2_cluster.command(0x0004, 0, level=75)
        assert rsp.status == foundation.Status.SUCCESS
        m1.assert_any_call(tcd_dimmer2_on)  # on_off
        m1.assert_called_with(tcd_dimmer2_level)  # current_level
        assert m1.call_count == 7

        # test `move_to_level_with_on_off` quirk (call on_off + current_level)
        rsp = await dimmer2_cluster.command(0x0004)
        assert rsp.status == foundation.Status.SUCCESS
        m1.assert_any_call(tcd_dimmer2_off)  # on_off
        m1.assert_called_with(tcd_dimmer2_level0)  # current_level
        assert m1.call_count == 9

        # test `move_to_level` quirk (only call current_level)
        rsp = await dimmer2_cluster.command(0x0000)
        assert rsp.status == foundation.Status.SUCCESS
        m1.assert_called_with(tcd_dimmer2_level0)  # current_level
        assert m1.call_count == 10

        # test `move_to_level` quirk (only call current_level)
        rsp = await dimmer2_cluster.command(0x0000, 75)
        assert rsp.status == foundation.Status.SUCCESS
        m1.assert_called_with(tcd_dimmer2_level)  # current_level
        assert m1.call_count == 11

        # test `move_to_level` quirk (only call current_level)
        rsp = await dimmer2_cluster.command(0x0000, level=75)
        assert rsp.status == foundation.Status.SUCCESS
        m1.assert_called_with(tcd_dimmer2_level)  # current_level
        assert m1.call_count == 12


async def test_tuya_mcu_classes():
    """Test tuya conversion from Data to ztype and reverse."""

    # Test TuyaDPType class
    assert len(TuyaDPType) == 6
    assert TuyaDPType.BOOL.ztype == t.Bool
    # no ztype for TuyaDPType.RAW
    assert not TuyaDPType.RAW.ztype
    assert TuyaDPType(3) == TuyaDPType.STRING

    # Test TuyaMCUCluster.MCUVersion class
    mcu_version = TuyaMCUCluster.MCUVersion.deserialize(b"\x00\x03\x82")[0]
    assert mcu_version
    assert mcu_version.tsn == 3
    assert mcu_version.version_raw == 130
    assert mcu_version.version == "2.0.2"
    mcu_version = TuyaMCUCluster.MCUVersion.deserialize(b"\x00\x04\x01")[0]
    assert mcu_version
    assert mcu_version.version_raw == 1
    assert mcu_version.version == "0.0.1"
    mcu_version = TuyaMCUCluster.MCUVersion.deserialize(b"\x00\x05\xFF")[0]
    assert mcu_version
    assert mcu_version.version_raw == 255
    assert mcu_version.version == "3.3.15"
    mcu_version = TuyaMCUCluster.MCUVersion()
    assert mcu_version
    assert not mcu_version.version

    # test TuyaClusterData.manufacturer values
    t_c_d = TuyaClusterData(manufacturer=foundation.ZCLHeader.NO_MANUFACTURER_ID)
    assert t_c_d.manufacturer == -1
    t_c_d = TuyaClusterData(manufacturer=4619)
    assert t_c_d.manufacturer == 4619
    t_c_d = TuyaClusterData(manufacturer="4098")
    assert t_c_d.manufacturer == 4098
    with pytest.raises(ValueError):
        TuyaClusterData(manufacturer="xiaomi")
    with pytest.raises(ValueError):
        TuyaClusterData(manufacturer=b"")
