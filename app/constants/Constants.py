
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
        insert or ignore into agents(accountId, symbol, headquarters, credits, startingFaction, shipCount, token) 
        values (?,?,?,?,?,?,?)
    """
    UPDATE_AGENT = """
        update agents
            set credits = (?),
            set shipCount = (?)
        where accountId = (?)
    """
    READ_TOKEN = "select token from agents where symbol = (?)"
    READ_AGENT = "select * from agents where symbol = (?)"
    READ_TRAITS = """select DISTINCT [traits.name]
        from waypoints 
        where (symbol = (?) and [traits.symbol] = (?))
        or (symbol = (?) and [traits.symbol] = (?))
    """
    SELECT_WAYPOINTS_FROM_SYSTEM = """
        select distinct systems."waypoints.symbol", replace(waypoints_traits_as_list.type, '_', ' ') as type, systems."waypoints.x", systems."waypoints.y", waypoints_traits_as_list.listof_traits
        from systems
        left join waypoints_traits_as_list
        on systems."waypoints.symbol" = waypoints_traits_as_list.symbol
        where systems.symbol = (?);
    """
    WAYPOINT_CHECK = "select symbol, systemSymbol from waypoints where symbol = (?)"