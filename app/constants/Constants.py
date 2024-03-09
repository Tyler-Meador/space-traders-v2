
class StyleConstants:
    FLEET_HEADER = "{ border: 1px solid rgba(49, 51, 63, 0.6); border-radius: 0.5rem; padding: calc(1em - 1px); background-color: #262730 }"
    FLEET_ROWS = "{ border-bottom: 1px solid rgba(49, 51, 63, 0.6); }"
    MARGIN_TOP_ZERO = "{ margin-top: 0px }"
    CONTROL_PANEL_WAYPOINT_INFO = "{ border-bottom: 1px solid rgba(49, 51, 63, 0.6); padding-top: 10px; padding-bottom: 10px; }"
    PADDING_TOP_5 = "{ padding-top: 5px; }"
    PADDING_TOP_15 = "{ padding-top: 15px; }"
    SHIP_INFO = "{ border-bottom: 1px solid rgba(49, 51, 63, 0.6); padding-bottom: 25px; padding-top:10px }"
    CONTROL_PANEL_DISPLAY = "{ border: 1px solid rgba(49, 51, 63, 0.6); border-radius: 30px; border-style: dashed; padding: calc(1em - 1px); }"

class NumConstants:
    LIGHTYEAR = 63241.1

class DB_CONSTANTS:
    INSERT_AGENT = """
        insert into Agent (accountId, symbol, headquarters, credits, startingFaction, shipCount, token) 
        values (?,?,?,?,?,?,?)
    """
    UPDATE_AGENT = """
        update Agent
            set credits = (?), shipCount = (?)
        where accountId = (?);
    """
    READ_TOKEN = "select token from Agent where symbol = (?)"
    READ_AGENT = "select * from Agent where symbol = (?)"
    READ_TRAITS_SHIPYARD_MARKETPLACE = """
        select w.symbol, t.name
        from Waypoints w
        inner join WaypointTraits wt
        on w.symbol = wt.waypoint_symbol
        inner join Traits t
        on wt.trait_id = t.trait_id
        where w.symbol = (?);
    """
    SELECT_WAYPOINT= """
        select symbol, type, x, y
        from Waypoints
        where Waypoints.system_symbol = (?);
    """
    WAYPOINT_CHECK = "select symbol, systemSymbol from waypoints where symbol = (?)"