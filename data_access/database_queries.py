# database_queries.py
# TO-DOs : Make venue_id into a paramter for all reports, and ecoaccount when necessary.
# Use get_revenues_details_data_query as an example

# Imports dictionary function
from analysis.functions.database_data import venues

def get_version_query():
    return "SELECT VERSION();"

####################################################################################

# No Filters exist for Personal Reports -> Logins report, only report needed is corp & management id
def get_personal_reports_logins_data_query(start_date, end_date):
    return start_date, end_date

#####################################################################################

# Bookings -> Bookings report category
# Only exists in management, so no differentiation between management & corporate needed
def get_booking_summary_data_query(start_date, end_date):
    return start_date, end_date
def get_booking_and_cancelled_data_query(start_date, end_date, venue):
    # Checks the venue dictionary to find the associated venue ids
    if venue in venues:
        venid = venues[venue]
    else:
        print("Venue not found in the dictionary.")

    return f"""
    WITH BookingData AS (
    SELECT
        (SELECT name FROM UrME.ECOaccounts WHERE id = party.resellerid) AS resellername,
        party.createuserid,
        party.id AS partyid,
        party.rndcode AS partycode,
        party.partyname,
        party.qty,
        party.totalamounts,
        party.venueid,
        party.caldate,
        FROM_UNIXTIME(party.createtstamp, '%%Y-%%m-%%d') AS createparty,
        CONCAT('ECZ', party.ecozone) AS ecozone,
        party.booktypes,
        party.globaltype,
        CASE 
            WHEN party.cancelstatus IS NOT NULL AND party.cancelstatus <> '' THEN party.cancelstatus
            WHEN party.operatestatus IS NOT NULL AND party.operatestatus <> '' THEN party.operatestatus
            WHEN party.reservestatus IS NOT NULL AND party.reservestatus <> '' THEN party.reservestatus
            ELSE NULL
        END AS currentstatus,
        party.email,
        party.phone,
        party.prepaidstatus,
        party.paytype,
        party.totalguests,
        party.ownerids,
        party.ownerid,
        party.sourcecode,
        party.sourceloc,
        party.originatorids,
        party.comment,
        party.shift,
        party.duration,
        party.instructions,
        GROUP_CONCAT(seat.locationid) AS locids,
        party.loyalty,
        party.insidetstamp,
        party.total,
        party.refby
    FROM
        BOOKING.PARTY AS party
    LEFT JOIN
        BOOKING.SEATING AS seat ON seat.partyid = party.id AND seat.status = 7
    WHERE
        party.caldate >= '{start_date}' AND
        party.caldate <= '{end_date}' AND
        party.status = '7' AND
        party.venueid IN (SELECT id FROM veadb.VENUEprofile WHERE manageentid = '{venid}')
    GROUP BY
        party.id
    ORDER BY
        party.caldate, party.venueid, party.ecozone
    )
    
    SELECT
        bd.createparty AS `Created Date`,
        bd.caldate AS `Event Date`,
        (SELECT name FROM UrME.ECOvenues WHERE veaid = bd.venueid LIMIT 1) AS `Venue`,
        bd.ecozone AS `EcoZone`,
        (SELECT name FROM veadb.EVENTprofile WHERE id = (
            SELECT eventid FROM veadb.EVENTdate WHERE venueid = bd.venueid AND caldate = bd.caldate AND ecozone = bd.ecozone AND status = '7' LIMIT 1
        ) LIMIT 1) AS `Event`,
        REPLACE(REPLACE(REPLACE(bd.partyname, '&#039;', "'"), '&#40;', "("), '&#41;', ")") as `Party Name`,
        bd.loyalty AS `Membership #`,
        bd.currentstatus AS `Current Status`,
        COALESCE(bd.shift, '') AS `Time`,
        DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(bd.insidetstamp), 'UTC', 'America/Los_Angeles'), '%%H:%%i') AS `Inside`,
        CASE
            WHEN bd.duration < 60 THEN CONCAT(bd.duration, 'm')
            WHEN bd.duration %% 60 > 0 THEN CONCAT(FLOOR(bd.duration / 60), 'h', bd.duration %% 60, 'm')
            ELSE CONCAT(FLOOR(bd.duration / 60), 'h')
        END AS `Duration`,
        bd.booktypes AS `Book Types`,
        bd.globaltype AS `Global Type`,
        bd.totalguests AS `Guests`,
        ROUND(bd.totalamounts / 100, 2) AS `Value`,
        bd.paytype AS `Pay Type`,
        ROUND(bd.total / 100, 2) AS `PrePay`,
        COALESCE(bd.prepaidstatus, 'None') AS `PrePaid Status`,
        bd.locids AS `Locations`,
        (SELECT fullname FROM UrME.USER WHERE id = bd.ownerids LIMIT 1) AS `Owners`,
        (SELECT fullname FROM UrME.USER WHERE id = bd.originatorids LIMIT 1) AS `Originators`,
        (SELECT fullname FROM UrME.USER WHERE id = bd.createuserid LIMIT 1) AS `User`,
        bd.refby AS `Referred By`,
        bd.resellername AS `Network`,
        COALESCE(CASE WHEN bd.sourcecode = 'microsite' THEN bd.sourceloc ELSE bd.sourcecode END) AS `Source`,
        bd.email AS `Email`,
        bd.phone AS `Phone`,
        bd.partyid AS `Res Code`,
        bd.partycode AS `Party Code`,
        bd.comment AS `Comment`,
        bd.instructions AS `Instruction`
    FROM
        BookingData bd
    ORDER BY
        bd.caldate;
    """
def get_booking_details_data_query(start_date, end_date, venue):
    # Checks the venue dictionary to find the associated venue ids
    if venue in venues:
        venid = venues[venue]
    else:
        print("Venue not found in the dictionary.")

    query = f""" 
        WITH BookingData AS (
            SELECT
                (SELECT name FROM UrME.ECOaccounts WHERE id = party.resellerid) AS resellername,
                party.createuserid,
                party.id AS partyid,
                party.rndcode AS partycode,
                party.partyname,
                party.qty,
                party.totalamounts,
                party.venueid,
                party.caldate,
                FROM_UNIXTIME(party.createtstamp, '%%Y-%%m-%%d') AS createparty,
                CONCAT('ECZ', party.ecozone) AS ecozone,
                party.booktypes,
                party.globaltype,
                CASE 
                    WHEN party.cancelstatus IS NOT NULL AND party.cancelstatus <> '' THEN party.cancelstatus
                    WHEN party.operatestatus IS NOT NULL AND party.operatestatus <> '' THEN party.operatestatus
                    WHEN party.reservestatus IS NOT NULL AND party.reservestatus <> '' THEN party.reservestatus
                    ELSE NULL
                END AS currentstatus,
                party.email,
                party.phone,
                party.prepaidstatus,
                party.paytype,
                party.totalguests,
                party.guests,
                party.ownerids,
                party.ownerid,
                party.sourcecode,
                party.sourceloc,
                party.originatorids,
                party.comment,
                party.shift,
                party.duration,
                party.instructions,
                GROUP_CONCAT(seat.locationid) AS locids,
                party.loyalty,
                party.insidetstamp,
                party.total,
                party.refby
            FROM
                BOOKING.PARTY AS party
            LEFT JOIN
                BOOKING.SEATING AS seat ON seat.partyid = party.id AND seat.status = 7
            WHERE
                party.caldate >= '{start_date}' AND
                party.caldate <= '{end_date}' AND
                party.status = '7' AND
                party.cancelstatus = '' AND
                party.venueid IN (SELECT id FROM veadb.VENUEprofile WHERE manageentid = '{venid}')
            GROUP BY
                party.id
            ORDER BY
                party.caldate, party.venueid, party.ecozone
        )
        
        SELECT
            bd.createparty AS "Created Date",
            bd.caldate AS "Event Date",
            (SELECT name FROM UrME.ECOvenues WHERE veaid = bd.venueid LIMIT 1) AS "Venue",
            bd.ecozone AS "EcoZone",
            (SELECT name FROM veadb.EVENTprofile WHERE id = (
                SELECT eventid FROM veadb.EVENTdate WHERE venueid = bd.venueid AND caldate = bd.caldate AND ecozone = bd.ecozone AND status = '7' LIMIT 1
            ) LIMIT 1) AS "Event",
            bd.partyname AS "Party Name",
            bd.loyalty AS "Membership #",
            bd.currentstatus AS "Current Status",
            DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(bd.insidetstamp), 'UTC', 'America/Los_Angeles'), '%%H:%%i') AS `Inside`,
            COALESCE(bd.shift, '') AS "Time",
            CASE
                WHEN bd.duration < 60 THEN CONCAT(bd.duration, 'm')
                WHEN bd.duration %% 60 > 0 THEN CONCAT(FLOOR(bd.duration / 60), 'h', bd.duration %% 60, 'm')
                ELSE CONCAT(FLOOR(bd.duration / 60), 'h')
            END AS "Duration",
            bd.booktypes AS "Book Types",
            bd.globaltype AS "Global Type",
            bd.guests * bd.qty AS "Guests",
            ROUND(bd.totalamounts / 100, 2) AS "Value",
            bd.paytype AS "Pay Type",
            ROUND(bd.total / 100, 2) AS `PrePay`,
            COALESCE(bd.prepaidstatus, 'None') AS "PrePaid Status",
            bd.locids AS "Locations",
            (SELECT fullname FROM UrME.USER WHERE id = bd.ownerids LIMIT 1) AS "Owners",
            (SELECT fullname FROM UrME.USER WHERE id = bd.originatorids LIMIT 1) AS "Originators",
            (SELECT fullname FROM UrME.USER WHERE id = bd.createuserid LIMIT 1) AS "User",
            bd.refby AS "Referred By",
            bd.resellername AS "Network",
            COALESCE(CASE WHEN bd.sourcecode = 'microsite' THEN bd.sourceloc ELSE bd.sourcecode END, '') AS "Source",
            bd.email AS "Email",
            bd.phone AS "Phone",
            bd.partyid AS "Res Code",
            bd.partycode AS "Party Code",
            bd.comment AS "Internal Notes",
            bd.instructions AS "Guest Notes"
        FROM
            BookingData bd
        ORDER BY
            bd.caldate;
            """
    return query
def get_promo_codes_data_query(start_date, end_date):
    return start_date, end_date

# Bookings -> Items report category
# Only exists in management, so no differentiation between management & corporate needed
def get_item_type_summary_data_query(start_date, end_date):
    return start_date, end_date
def get_bookings_item_summary_data_query(start_date, end_date):
    return start_date, end_date
def get_item_details_data_query(start_date, end_date, venue):
    # Checks the venue dictionary to find the associated venue ids
    if venue in venues:
        venid = venues[venue]
    else:
        print("Venue not found in the dictionary.")

    # Query string, constructed using start date, end date passed through the function, and then venue_id is found through looking in the
    # "venues" dictionary
    query = f"""
        WITH BookingData AS (
        SELECT
            party.createuserid,
            party.id AS partyid,
            party.rndcode AS partycode,
            party.partyname,
            party.baseagree,
            party.paid,
            party.loyalty,
            party.qty AS partyqty,
            party.totalamounts,
            party.venueid,
            party.caldate,
            FROM_UNIXTIME(party.createtstamp, '%%Y-%%m-%%d') AS createparty,
            CONCAT('ECZ', party.ecozone) AS ecozone,
            CASE 
                WHEN party.cancelstatus IS NOT NULL AND party.cancelstatus <> '' THEN party.cancelstatus
                WHEN party.operatestatus IS NOT NULL AND party.operatestatus <> '' THEN party.operatestatus
                WHEN party.reservestatus IS NOT NULL AND party.reservestatus <> '' THEN party.reservestatus
                ELSE NULL
            END AS currentstatus,
            party.refby,
            party.email,
            party.phone,
            party.prepaidstatus,
            party.paymentstatus,
            party.reservestatus,
            party.cancelstatus,
            party.operatestatus,
            party.totalguests AS partytotalguests,
            party.ownerids,
            party.ownerid,
            party.sourcecode,
            party.sourceloc,
            party.originatorids,
            party.comment,
            party.shift,
            party.duration,
            party.instructions,
            party.booktypes AS pbooktypes,
            party.globaltype AS pglobaltype,
            party.paytype AS ppaytype,
            GROUP_CONCAT(seat.locationid) AS locids,
            bk.subtotal,
            bk.itemname AS bitemname,
            (bk.guests * bk.qty) as itemguests,
            bk.qty AS bkqty,
            bk.booktypeid,
            bk.globaltype AS bkglobaltype,
            bk.paytype AS bkpaytype,
            bk.baseagree as value,
            bk.masteritemid,
            bk.pricing
        FROM
            BOOKING.PARTY AS party
        LEFT JOIN
            BOOKING.SEATING AS seat ON seat.partyid = party.id AND seat.status = 7
        LEFT JOIN
            BOOKING.BOOKING AS bk ON bk.partyid = party.id AND bk.status = 7
        WHERE
            party.caldate >= '{start_date}' AND 
            party.caldate <= '{end_date}' AND 
            party.status = '7' AND 
            party.cancelstatus = '' AND
            party.venueid IN (SELECT id FROM veadb.VENUEprofile WHERE manageentid = '{venid}')
        GROUP BY
            bk.id, party.id
        )
    
        SELECT
            bd.bitemname AS "Item Name",
            COALESCE(
            (SELECT 
                CASE
                    WHEN mi.itcfix IS NOT NULL AND mi.itcfix <> '' THEN CONCAT(mi.itcode, '-', mi.itcfix) 
                    ELSE mi.itcode
                END
             FROM UrInventory.MASTERitem mi 
             WHERE mi.id = bd.masteritemid AND mi.status = '7' AND mi.itcode <> '0' AND mi.itcode <> ''
             LIMIT 1),
            '') AS "Item Code",
            bd.createparty AS "Created Date",
            bd.caldate AS "Event Date",
            (SELECT name FROM UrME.ECOvenues WHERE veaid = bd.venueid LIMIT 1) AS "Venue",
            bd.ecozone AS "EcoZone",
            (SELECT name FROM veadb.EVENTprofile WHERE id = (
                SELECT eventid FROM veadb.EVENTdate WHERE venueid = bd.venueid AND caldate = bd.caldate AND ecozone = bd.ecozone AND status = '7' LIMIT 1
            ) LIMIT 1) AS "Event",
            bd.partyname AS "Party Name",
            bd.loyalty AS "Membership #",
            bd.currentstatus AS "Current Status",
            COALESCE(bd.shift, '') AS "Time",
            CASE
                WHEN bd.duration < 60 THEN CONCAT(bd.duration, 'm')
                WHEN bd.duration %% 60 > 0 THEN CONCAT(FLOOR(bd.duration / 60), 'h', MOD(bd.duration, 60), 'm')
                ELSE CONCAT(FLOOR(bd.duration / 60), 'h')
            END AS "Duration",
            COALESCE((SELECT name FROM UrInventory.BOOKtype WHERE id = bd.booktypeid), bd.pbooktypes) AS "Book Type",
            COALESCE(bd.bkglobaltype, bd.pglobaltype) AS "Global Type",
            COALESCE(bd.bkqty, bd.partyqty) AS "Qty",
            COALESCE(bd.itemguests, bd.partytotalguests) AS "Guests",
            COALESCE(bd.bkpaytype, bd.ppaytype) AS "Pay Type",
            bd.pricing AS "Pricing",
            ROUND(bd.subtotal / 100, 2) AS "PrePay Subtotal",
            ROUND(bd.value / 100, 2) AS "Agreement",
            bd.paymentstatus AS "PrePaid Status",
            -- (SELECT GROUP_CONCAT(name SEPARATOR ', ') FROM UrME.LOCATION WHERE id IN (SELECT locationid FROM BOOKING.SEATING WHERE partyid = bd.partyid)) AS "Locations",
            bd.locids AS "Locations",
            (SELECT fullname FROM UrME.USER WHERE id = (SUBSTRING_INDEX(bd.ownerids, ',', 1))) AS "Owners",
            (SELECT fullname FROM UrME.USER WHERE id = (SUBSTRING_INDEX(bd.originatorids, ',', 1))) AS "Originators",
            (SELECT fullname FROM UrME.USER WHERE id = bd.createuserid) AS "User",
            bd.refby AS "Referred By",
            bd.sourcecode AS "Source",
            bd.email AS "Email",
            bd.phone AS "Phone",
            bd.partyid AS "Res Code",
            bd.partycode AS "Party Code",
            bd.comment AS "Comment",
            bd.instructions AS "Instruction"
        FROM
            BookingData bd
        ORDER BY
            bd.caldate, bd.venueid, bd.ecozone;
            """
    return query
def get_item_updates_data_query(start_date, end_date):
    return start_date, end_date

# Bookings -> Carriers report category
# Only exists in management, so no differentiation between management & corporate needed
def get_day_carrier_types_data_query(start_date, end_date):
    return start_date, end_date
def get_day_carrier_bookings_data_query(start_date, end_date):
    return start_date, end_date

#######################################################################################

# Payment Gateway -> Gateway (ONLY Corporate)
# A module in payment gateway that ONLY exists in corporate, no need for paramter to determine that
def get_daily_transactions_data_query(start_date, end_date):
    return start_date, end_date
def get_daily_summary_data_query(start_date, end_date):
    return start_date, end_date

# Payment Gateway -> Sales
# Exists in BOTH management & corporate, so parameter determining that is going to be needed
def get_payment_sales_summary_data_query(start_date, end_date):
    return start_date, end_date
def get_daily_sales_summary_data_query(start_date, end_date):
    return start_date, end_date
def get_recent_sales_data_query(start_date, end_date):
    return start_date, end_date
def get_sales_details_data_query(start_date, end_date, ecosystem, venue):
    # Checks the venue dictionary to find the associated venue ids
    if venue in venues:
        venid = venues[venue]
    else:
        print("Venue not found in the dictionary.")

    # Determines join condition based off of ecosystem
    if ecosystem == ('management' or 'box-ecosystem-23'):
        venue_condition = f"tx.venueid IN (SELECT id FROM veadb.VENUEprofile WHERE manageentid = '{venid}')"
    elif ecosystem == ('corporate' or 'box-ecosystem-28'):
        venue_condition = f"tx.venueid IN (SELECT id FROM veadb.VENUEprofile WHERE corpentid = '{venid}')"
    else:
        # Default condition
        venue_condition = f"tx.venueid IN (SELECT id FROM veadb.VENUEprofile WHERE corpentid = '{venid}')"
    # Query string, constructed using start date, end date passed through the function, with dynamic
    # Join condition based off of ecosystem parameter, and then venue_id is found through looking in the
    # "venues" dictionary
    query = f""" 
            WITH pre AS (
            SELECT 
                sum(tb.guests) as guests, 
                sum(tb.appfee) as appfee, 
                sum(subtotal) as subtotal, 
                sum(subtotalagree) as subtotalagree, 
                sum(tb.qty) as qty, 
                tx.itemname, 
                tb.pricingtype, 
                tx.bookcode, 
                tb.booktypeid, 
                tb.globaltype, 
                tx.caldate, 
                tr.transdate, 
                tr.confcode, 
                tb.createtstamp as created, 
                tb.venueid, 
                tb.transid, 
                tb.ecozone, 
                tb.rndcode as transbookcode, 
                tr.gxnordercode, 
                tb.action, 
                tr.authcode, 
                tr.cardtoken, 
                tr.cartcode, 
                tb.id as transbookid,
                tr.currency, 
                tr.rndcode as transcode, 
                tr.gatewaycode, 
                tr.gateway, 
                tr.paymethod, 
                tr.paytransport, 
                CONCAT('***', tr.billing_last4, ' exp ', tr.billing_exp) as payref, 
                tr.billing_ccbrand as paybrand, 
                tr.billing_name as payname, 
                tr.partyname, 
                sum(tb.total) as amount, 
                tb.partycode,
                v.name,
                b.name as booktypename
            FROM PAY.TRANSbook as tb
            JOIN PAY.TIX as tx on tx.id=tb.tixid and {venue_condition}
            LEFT JOIN PAY.TRANS as tr on tr.id=tb.transid and tr.status=7
            JOIN veadb.VENUEprofile v ON v.id = tb.venueid
            JOIN UrInventory.BOOKtype b ON b.id = tb.booktypeid  and b.status='7'
            WHERE 
                tb.transdate>='{start_date}' and
                tb.transdate<='{end_date}' and
                (tb.subtotal<>0 or tb.charge<>0) and
                tb.status=7
            GROUP BY tb.id
            ORDER BY tb.createtstamp DESC)

            SELECT 
                p.transdate as `Trans Date`,	
                concat(from_unixtime(p.created, '%%h:%%i%%p'), " PST") as `Trans Time`,
                p.name as `Venue`,
                p.ecozone as `EcoZone`,
                p.caldate as `Event Date`,
                p.currency as `Currency`,		
                ROUND(p.subtotal / 100, 2)  as `Prepaid`,
                ROUND(p.subtotalagree / 100, 2) as `Agreed`,
                ROUND(p.amount / 100, 2) as `Charged`,
                p.action as `Action`,	
                p.itemname as `item`,
                p.booktypename as `booktype`,
                p.globaltype as `globaltype`,
                p.pricingtype as `pricing`,
                p.qty as `qty`,
                p.guests as `guests`,
                p.gateway as `Processor`,
                p.paymethod as `Method`,
                p.paytransport as `Transport`,
                p.payref as `Reference`,		
                p.paybrand as `Brand`,
                p.payname as `Payor Name`,
                p.partyname as `Party Name`,
                p.gatewaycode as `Gateway Code`,	
                p.authcode as `Auth Code`,
                p.cardtoken as `Card Token`,
                p.bookcode as `Book Code`,	
                p.confcode as `Conf Code`,
                p.transid as `Trans ID`,
                p.transbookid as `Trans Book ID`,
                p.gxnordercode as `Order Code`
            FROM
                pre as p;
        """
    return query
def get_sales_breakdown_data_query(start_date, end_date, ecosystem, venue):
    # Checks the venue dictionary to find the associated venue ids
    if venue in venues:
        venid = venues[venue]
    else:
        print("Venue not found in the dictionary.")

    # Determines join condition based off of ecosystem
    if ecosystem == ('management' or 'box-ecosystem-23'):
        venue_condition = f"tx.venueid IN (SELECT id FROM veadb.VENUEprofile WHERE manageentid = '{venid}')"
    elif ecosystem == ('corporate' or 'box-ecosystem-28'):
        venue_condition = f"tx.venueid IN (SELECT id FROM veadb.VENUEprofile WHERE corpentid = '{venid}')"
    else:
        # Default condition
        venue_condition = f"tx.venueid IN (SELECT id FROM veadb.VENUEprofile WHERE corpentid = '{venid}')"
    # Query string, constructed using start date, end date passed through the function, with dynamic
    # Join condition based off of ecosystem parameter, and then venue_id is found through looking in the
    # "venues" dictionary
    query = f""" 
        WITH pre AS (
        SELECT 
            sum(tb.guests) as guests, 
            sum(tb.appfee) as appfee, 
            sum(subtotal) as subtotal, 
            sum(subtotalagree) as subtotalagree, 
            sum(tb.qty) as qty, 
            tx.itemname, 
            tb.pricingtype, 
            tx.bookcode, 
            tb.booktypeid, 
            tb.globaltype, 
            tx.caldate, 
            tr.transdate, 
            tr.confcode, 
            tb.createtstamp as created, 
            tb.venueid, 
            tb.transid, 
            tb.ecozone, 
            tb.rndcode as transbookcode, 
            tr.gxnordercode, 
            tb.action, 
            tr.authcode, 
            tr.cardtoken, 
            tr.cartcode, 
            tb.id as transbookid,
            tr.currency, 
            tr.rndcode as transcode, 
            tr.gatewaycode, 
            tr.gateway, 
            tr.paymethod, 
            tr.paytransport, 
            CONCAT('***', tr.billing_last4, ' exp ', tr.billing_exp) as payref, 
            tr.billing_ccbrand as paybrand, 
            tr.billing_name as payname, 
            tr.partyname, 
            sum(tb.total) as amount, 
            tb.partycode,
            v.name,
            b.name as booktypename,
            tb.surcharge,
            tb.procfee,
            tb.merchantfee,
            tb.procfeetax,
            tb.breakdown,
            tb.total
        FROM PAY.TRANSbook as tb
        JOIN PAY.TIX as tx on tx.id=tb.tixid and {venue_condition}
        LEFT JOIN PAY.TRANS as tr on tr.id=tb.transid and tr.status=7
        JOIN veadb.VENUEprofile v ON v.id = tb.venueid
        JOIN UrInventory.BOOKtype b ON b.id = tb.booktypeid  and b.status='7'
        WHERE 
            tb.transdate>='{start_date}' and
            tb.transdate<='{end_date}' and
            (tb.subtotal<>0 or tb.charge<>0) and
            tb.status=7
        GROUP BY tb.id
        ORDER BY tb.createtstamp DESC)

        SELECT 
            p.transdate as `Trans Date`,
            p.name as `Venue`,
            p.ecozone as `EcoZone`,
            p.caldate as `Event Date`,
            p.currency as `Currency`,		
            ROUND(p.subtotal / 100, 2)  as `Prepaid`,
            ROUND(p.subtotalagree / 100, 2) as `Agreed`,
            ROUND(p.amount / 100, 2) as `Charged`,
            p.action as `Action`,	
            p.itemname as `item`,
            p.booktypename as `booktype`,
            p.globaltype as `globaltype`,
            p.pricingtype as `pricing`,
            p.qty as `qty`,
            p.guests as `guests`,
            p.payname as `Payor Name`,
            p.partyname as `Party Name`,
            p.confcode as  `Conf Code`,
            p.authcode as `Auth Code`,
            p.bookcode as `Book Code`,
            p.transid as `Trans ID`,
            p.gxnordercode as `Order Code`,
            ROUND(p.appfee / 100, 2) as `UV App Fee`,
            0 as `Merchant Fee`, -- p.appfee is a place holder, logic for this column is only calculated after BreakDown is calculated. 
            p.breakdown as `BreakDown`
        FROM
            pre as p;
            """
    return query

# Payment Gateway -> Revenue
# Exists in BOTH management & corporate, so paramter determing that is going to be needed
def get_event_summary_data_query(start_date, end_date):
    return start_date, end_date
def get_breakdown_summary_data_query(start_date, end_date):
    return start_date, end_date
def get_pricing_summary_data_query(start_date, end_date):
    return start_date, end_date
def get_book_type_summary_data_query(start_date, end_date):
    return start_date, end_date
def get_payment_item_summary_data_query(start_date, end_date):
    return start_date, end_date
def get_owner_summary_data_query(start_date, end_date):
    return start_date, end_date
def get_item_breakdown_data_query(start_date, end_date):
    return start_date, end_date
def get_item_price_points_data_query(start_date, end_date):
    return start_date, end_date
def get_pay_media_summary_data_query(start_date, end_date):
    return f"""
    WITH initial AS (
	SELECT
		 sum(tb.guests) as guests, sum(tb.qty) as qty, sum(subtotal) as subtotal, 
		 sum(subtotalagree) as subtotalagree, tx.itemname, tx.bookcode, tb.booktypeid, 
		 tb.globaltype, tx.caldate, tr.transdate, tr.confcode, tb.id as transbookid, 
		tb.createtstamp, tb.venueid, tb.transid, tb.rndcode as transbookcode, 
		tr.gxnordercode, tb.action, tr.authcode, tr.cardtoken, tr.cartcode,
		 tr.currency, tr.rndcode as transcode, tr.gatewaycode, tr.gateway, tr.paymethod, 
		 tr.paytransport, CONCAT('***', tr.billing_last4, ' exp ', tr.billing_exp) as payref, 
 		tr.billing_ccbrand as paybrand, tr.billing_name as payname, 
 		tr.partyname, sum(tb.total) as amount, tb.partycode, v.name as `venuename`
	FROM PAY.TRANSbook as tb 
	JOIN PAY.TIX as tx on tx.id=tb.tixid and tx.venueid in (SELECT id FROM veadb.VENUEprofile WHERE corpentid = '130')
	LEFT JOIN PAY.TRANS as tr on tr.id=tb.transid and tr.status=7
	JOIN veadb.VENUEprofile v ON v.id = tb.venueid
	JOIN UrInventory.BOOKtype b ON b.id = tb.booktypeid  and b.status='7'
	WHERE
	tb.caldate>='{start_date}' AND
	tb.caldate<='{end_date}' AND
	tb.transdate<=tb.caldate AND
	tb.status=7 AND
	(tb.subtotal<>0 or tb.charge<>0) AND
	tb.globaltype IS NOT NULL
	GROUP BY tb.venueid, tr.currency, tb.action, tb.globaltype, tr.gatewaycode, tr.paymethod, tr.paytransport, tr.billing_ccbrand
	ORDER BY tb.createtstamp DESC
    )

    SELECT
	    venuename as `Venue`,
	    currency as `Currency`,
	    SUM(subtotal) / 100 as `Prepaid`,
	    SUM(subtotalagree) / 100 as `Agreed`,
	    SUM(amount) / 100 as `Charged`,
	    action as `Action`,
	    globaltype as `Global Type`,
	    SUM(qty) as `qty`,
	    SUM(guests) as `guests`,
	    gateway as `Processor`,
	    paymethod as `Method`,
	    paytransport as `Transport`,
	    paybrand as `Brand`
    FROM
	    initial
    GROUP BY paybrand, `action`, globaltype, venue;
        """
def get_future_sales_data_query(start_date, end_date):
    return start_date, end_date
# Planning to add venid to all venues, will probably first have it as venue, and it looks in a dictionary to find the corresponding venue ids
def get_revenue_details_data_query(start_date, end_date, ecosystem, venue):
    # Checks the venue dictionary to find the associated venue ids
    if venue in venues:
        venid = venues[venue]
    else:
        print("Venue not found in the dictionary.")

    # Determines join condition based off of ecosystem
    if ecosystem == ('management' or 'box-ecosystem-23'):
        venue_condition = f"tx.venueid IN (SELECT id FROM veadb.VENUEprofile WHERE manageentid = '{venid}')"
    elif ecosystem == ('corporate' or 'box-ecosystem-28'):
        venue_condition = f"tx.venueid IN (SELECT id FROM veadb.VENUEprofile WHERE corpentid = '{venid}')"
    else:
        # Default condition
        venue_condition = f"tx.venueid IN (SELECT id FROM veadb.VENUEprofile WHERE corpentid = '{venid}')"
    # Query string, constructed using start date, end date passed through the function, with dynamic
    # Join condition based off of ecosystem parameter, and then venue_id is found through looking in the
    # "venues" dictionary
    query = f""" 
        WITH pre AS (
        SELECT 
            sum(tb.guests) as guests, 
            sum(tb.appfee) as appfee, 
            sum(subtotal) as subtotal, 
            sum(subtotalagree) as subtotalagree, 
            sum(tb.qty) as qty, 
            tx.itemname, 
            tb.pricingtype, 
            tx.bookcode, 
            tb.booktypeid, 
            tb.globaltype, 
            tx.caldate, 
            tr.transdate, 
            tr.confcode, 
            tb.createtstamp as created, 
            tb.venueid, 
            tb.transid, 
            tb.ecozone, 
            tb.rndcode as transbookcode, 
            tr.gxnordercode, 
            tb.action, 
            tr.authcode, 
            tr.cardtoken, 
            tr.cartcode, 
            tb.id as transbookid,
            tr.currency, 
            tr.rndcode as transcode, 
            tr.gatewaycode, 
            tr.gateway, 
            tr.paymethod, 
            tr.paytransport, 
            CONCAT('***', tr.billing_last4, ' exp ', tr.billing_exp) as payref, 
            tr.billing_ccbrand as paybrand, 
            tr.billing_name as payname, 
            tr.partyname, 
            sum(tb.total) as amount, 
            tb.partycode,
            v.name,
            b.name as booktypename
        FROM PAY.TRANSbook as tb
        JOIN PAY.TIX as tx on tx.id=tb.tixid and {venue_condition}
        LEFT JOIN PAY.TRANS as tr on tr.id=tb.transid and tr.status=7
        JOIN veadb.VENUEprofile v ON v.id = tb.venueid
        JOIN UrInventory.BOOKtype b ON b.id = tb.booktypeid  and b.status='7'
        WHERE 
            tb.caldate>='{start_date}' and
            tb.caldate<='{end_date}' and
            tb.transdate<=tb.caldate and
            (tb.subtotal<>0 or tb.charge<>0) and
            tb.status=7
        GROUP BY tb.id
        ORDER BY tb.createtstamp DESC)
        
        SELECT 
            p.transdate as `Trans Date`,	
            concat(from_unixtime(p.created, '%%h:%%i%%p'), " PST") as `Trans Time`,
            p.name as `Venue`,
            p.ecozone as `EcoZone`,
            p.caldate as `Event Date`,
            p.currency as `Currency`,		
            ROUND(p.subtotal / 100, 2)  as `Prepaid`,
            ROUND(p.subtotalagree / 100, 2) as `Agreed`,
            ROUND(p.amount / 100, 2) as `Charged`,
            p.action as `Action`,	
            p.itemname as `item`,
            p.booktypename as `booktype`,
            p.globaltype as `globaltype`,
            p.pricingtype as `pricing`,
            p.qty as `qty`,
            p.guests as `guests`,
            p.gateway as `Processor`,
            p.paymethod as `Method`,
            p.paytransport as `Transport`,
            p.payref as `Reference`,		
            p.paybrand as `Brand`,
            p.payname as `Payor Name`,
            p.partyname as `Party Name`,
            p.gatewaycode as `Gateway Code`,	
            p.authcode as `Auth Code`,
            p.cardtoken as `Card Token`,
            p.bookcode as `Book Code`,	
            p.confcode as `Conf Code`,
            p.transid as `Trans ID`,
            p.transbookid as `Trans Book ID`,
            p.gxnordercode as `Order Code`
        FROM
            pre as p;
    """
    return query
# UPDATE QUERY BELOW WHEN PROC SURCHARCES IS FIXED
def get_revenue_breakdown_data_query(start_date, end_date, ecosystem, venue):
    # Checks the venue dictionary to find the associated venue ids
    if venue in venues:
        venid = venues[venue]
    else:
        print("Venue not found in the dictionary.")

    # Determines join condition based off of ecosystem
    if ecosystem == ('management' or 'box-ecosystem-23'):
        venue_condition = f"tx.venueid IN (SELECT id FROM veadb.VENUEprofile WHERE manageentid = '{venid}')"
    elif ecosystem == ('corporate' or 'box-ecosystem-28'):
        venue_condition = f"tx.venueid IN (SELECT id FROM veadb.VENUEprofile WHERE corpentid = '{venid}')"
    else:
        # Default condition
        venue_condition = f"tx.venueid IN (SELECT id FROM veadb.VENUEprofile WHERE corpentid = '{venid}')"
    # Query string, constructed using start date, end date passed through the function, with dynamic
    # Join condition based off of ecosystem parameter, and then venue_id is found through looking in the
    # "venues" dictionary
    query = f""" 
    WITH pre AS (
    SELECT 
        sum(tb.guests) as guests, 
        sum(tb.appfee) as appfee, 
        sum(subtotal) as subtotal, 
        sum(subtotalagree) as subtotalagree, 
        sum(tb.qty) as qty, 
        tx.itemname, 
        tb.pricingtype, 
        tx.bookcode, 
        tb.booktypeid, 
        tb.globaltype, 
        tx.caldate, 
        tr.transdate, 
        tr.confcode, 
        tb.createtstamp as created, 
        tb.venueid, 
        tb.transid, 
        tb.ecozone, 
        tb.rndcode as transbookcode, 
        tr.gxnordercode, 
        tb.action, 
        tr.authcode, 
        tr.cardtoken, 
        tr.cartcode, 
        tb.id as transbookid,
        tr.currency, 
        tr.rndcode as transcode, 
        tr.gatewaycode, 
        tr.gateway, 
        tr.paymethod, 
        tr.paytransport, 
        CONCAT('***', tr.billing_last4, ' exp ', tr.billing_exp) as payref, 
        tr.billing_ccbrand as paybrand, 
        tr.billing_name as payname, 
        tr.partyname, 
        sum(tb.total) as amount, 
        tb.partycode,
        v.name,
        b.name as booktypename,
        tb.surcharge,
        tb.procfee,
        tb.merchantfee,
        tb.procfeetax,
        tb.breakdown,
        tb.total
    FROM PAY.TRANSbook as tb
    JOIN PAY.TIX as tx on tx.id=tb.tixid and {venue_condition}
    LEFT JOIN PAY.TRANS as tr on tr.id=tb.transid and tr.status=7
    JOIN veadb.VENUEprofile v ON v.id = tb.venueid
    JOIN UrInventory.BOOKtype b ON b.id = tb.booktypeid  and b.status='7'
    WHERE 
        tb.caldate>='{start_date}' and
        tb.caldate<='{end_date}' and
        tb.transdate<=tb.caldate and
        (tb.subtotal<>0 or tb.charge<>0) and
        tb.status=7
    GROUP BY tb.id
    ORDER BY tb.createtstamp DESC)
        
    SELECT 
        p.transdate as `Trans Date`,
        p.name as `Venue`,
        p.ecozone as `EcoZone`,
        p.caldate as `Event Date`,
        (SELECT name FROM veadb.EVENTprofile WHERE id = (
            SELECT eventid FROM veadb.EVENTdate WHERE venueid = p.venueid AND caldate = p.caldate AND ecozone = p.ecozone AND status = '7' LIMIT 1
        ) LIMIT 1) AS `Event`,
        p.currency as `Currency`,		
        ROUND(p.subtotal / 100, 2)  as `Prepaid`,
        ROUND(p.subtotalagree / 100, 2) as `Agreed`,
        ROUND(p.amount / 100, 2) as `Charged`,
        p.action as `Action`,	
        p.itemname as `item`,
        p.booktypename as `booktype`,
        p.globaltype as `globaltype`,
        p.pricingtype as `pricing`,
        p.qty as `qty`,
        p.guests as `guests`,
        p.payname as `Payor Name`,
        p.partyname as `Party Name`,
        p.authcode as `Auth Code`,
        p.bookcode as `Book Code`,
        p.transid as `Trans ID`,
        p.gxnordercode as `Order Code`,
        ROUND(p.procfee / 100, 2) as `Proc Surcharces`,
        ROUND(p.appfee / 100, 2) as `UV App Fee`,
        ROUND(p.amount / 100 * .03, 2) as `Est. Merchant Fee`,
        ROUND((p.procfee - (p.amount * .03) - p.appfee) / 100, 2) as `Est. Proc Sur Profit`,
        p.breakdown as `BreakDown`
    FROM
        pre as p;
        """
    return query

# Payment Gateway -> Adjustments
# Exists in BOTH management & corporate, so parameter determining that is going to be needed
def get_adjustment_details_data_query(start_date, end_date):
    return start_date, end_date

# Payment Gateway -> Total Revenues
# Exists in BOTH management & corporate, so parameter determining that is going to be needed
def get_total_event_summary_data_query(start_date, end_date):
    return start_date, end_date
def get_total_revenues_details_data_query(start_date, end_date):
    return start_date, end_date
def get_total_revenues_breakdown_data_query(start_date, end_date):
    return f"""
    WITH pre AS (
    SELECT 
    	sum(tb.guests) as guests, sum(tb.appfee) as appfee, sum(subtotal) as subtotal, sum(subtotalagree) as subtotalagree, sum(tb.qty) as qty, 
    	tx.itemname, tb.pricingtype, tx.bookcode, tb.booktypeid, tb.globaltype, tx.caldate, tr.transdate, tr.confcode,
    	tb.createtstamp as created, tb.venueid, tb.transid, tb.ecozone, tb.rndcode as transbookcode, tr.gxnordercode, tb.action, 
    	tr.authcode, tr.cardtoken, tr.cartcode, tb.id as transbookid,tr.currency, tr.rndcode as transcode, tr.gatewaycode, tr.gateway, tr.paymethod, tr.paytransport, 
     	CONCAT('***', tr.billing_last4, ' exp ', tr.billing_exp) as payref, tr.billing_ccbrand as paybrand, tr.billing_name as payname, tr.partyname, sum(tb.total) as amount, 
     	tb.partycode, v.name, b.name as booktypename, tb.surcharge, tb.procfee,
     	tb.merchantfee, tb.procfeetax, tb.breakdown, tb.total
    FROM PAY.TRANSbook as tb
    JOIN PAY.TIX as tx on tx.id=tb.tixid and tx.venueid in (SELECT id FROM veadb.VENUEprofile WHERE corpentid = '130')
    LEFT JOIN PAY.TRANS as tr on tr.id=tb.transid and tr.status=7
    JOIN veadb.VENUEprofile v ON v.id = tb.venueid
    JOIN UrInventory.BOOKtype b ON b.id = tb.booktypeid  and b.status='7'
    WHERE 
    	tb.caldate>='{start_date}' and
    	tb.caldate<='{end_date}' and
    	(tb.subtotal<>0 or tb.charge<>0) and
    	tb.status=7
    GROUP BY tb.id
    ORDER BY tb.createtstamp DESC)

    SELECT 
    	p.transdate as `Trans Date`,
    	REPLACE(REPLACE(REPLACE(p.name, '&#039;', "'"), '&#40;', "("), '&#41;', ")") as `Venue`,
    	p.ecozone as `EcoZone`,
    	p.caldate as `Event Date`,
    	NULL as `Event`,
    	p.currency as `Currency`,		
    	p.subtotal / 100  as `Prepaid`,
    	p.subtotalagree / 100 as `Agreed`,
    	p.amount / 100 as `Charged`,
    	p.action as `Action`,	
    	REPLACE(REPLACE(REPLACE(p.itemname, '&#039;', "'"), '&#40;', "("), '&#41;', ")") as `item`,
    	p.booktypename as `booktype`,
    	p.globaltype as `globaltype`,
    	p.pricingtype as `pricing`,
    	p.qty as `qty`,
    	p.guests as `guests`,
    	REPLACE(REPLACE(REPLACE(p.payname, '&#039;', "'"), '&#40;', "("), '&#41;', ")") as `Payor Name`,
    	p.partyname as `Party Name`,
    	p.authcode as `Auth Code`,
    	p.bookcode as `Book Code`,
    	p.transid as `Trans ID`,
    	p.gxnordercode as `Order Code`,
    	p.breakdown as `BreakDown`
    FROM
    	pre as p;
        """
def get_total_itemized_data_query(start_date, end_date):
    return start_date, end_date

# Payment Gateway -> GCB Sales
# Exists in BOTH management & corporate, so parameter determing that is going to be neeeded
def get_gcb_sales_summary_data_query(start_date, end_date):
    return start_date, end_date
def get_gcb_sales_details_data_query(start_date, end_date):
    return start_date, end_date
def get_sales_adjustments_data_query(start_date, end_date):
    return start_date, end_date

# Payment Gateway -> GCB Revenues
# Exists in BOTH management & corporate, so paramter determing that is going to be needed
def get_revenue_summary_data_query(start_date, end_date):
    return start_date, end_date
def get_gcb_revenue_details_data_query(start_date, end_date):
    return start_date, end_date
def get_revenue_adjustments_data_query(start_date, end_date):
    return start_date, end_date
def get_total_revenue_data_query(start_date, end_date):
    return start_date, end_date
def get_total_revenue_detail_data_query(start_date, end_date):
    return start_date, end_date
def get_future_revenue_data_query(start_date, end_date):
    return start_date, end_date
def get_admission_tendered_data_query(start_date, end_date):
    return start_date, end_date

######################################################################################

# CRM -> Emails, Top 100, Top 1,000
# Exists in ONLY management, no parameter needed
def get_emails_data_query(start_date, end_date):
    return start_date, end_date
def get_emails_top_100_data_query(start_date, end_date):
    return start_date, end_date
def get_emails_top_1000_data_query(start_date, end_date):
    return start_date, end_date

#######################################################################################

# Disputes -> Disputes
# Exists in BOTH management & corporate, parameter needed for that
def get_disputes_data_query(start_date, end_date):
    return start_date, end_date

#######################################################################################

# Refunds -> Requests, By Transaction, By Event Date
# Exists in ONLY management, no parameter needed
def get_requests_data_query(start_date, end_date):
    return start_date, end_date
def get_requests_by_transaction_data_query(start_date, end_date):
    return start_date, end_date
def get_requests_by_event_date_data_query(start_date, end_date):
    return start_date, end_date

######################################################################################

# POS -> Check Matching
# Exists in ONLY management, no parameter needed
def get_all_checks_data_query(start_date, end_date):
    return start_date, end_date
def get_unmatched_checks_data_query(start_date, end_date):
    return start_date, end_date
def get_matched_checks_data_query(start_date, end_date):
    return start_date, end_date
def get_matched_parties_data_query(start_date, end_date):
    return start_date, end_date

# POS -> Ranking Reports
# Exists in ONLY management, parameter not needed
def get_direct_owner_ranking_data_query(start_date, end_date):
    return start_date, end_date
def get_all_owners_ranking_data_query(start_date, end_date):
    return start_date, end_date
def get_originators_ranking_data_query(start_date, end_date):
    return start_date, end_date
def get_comp_ranking_data_query(start_date, end_date):
    return start_date, end_date

# POS -> Venue Revenues
# Exists in ONLY management, parameter not needed
def get_checktype_overview_data_query(start_date, end_date):
    return start_date, end_date
def get_check_category_overview_data_query(start_date, end_date):
    return start_date, end_date
def get_tender_overview_data_query(start_date, end_date):
    return start_date, end_date

#######################################################################################

# Finance Reconciliation -> Dail Summary (Typo on front-end)
# Exists in ONLY corporate, parameter not needed
def get_finance_daily_summary_data_query(start_date, end_date):
    return start_date, end_date
def get_transaction_details_data_query(start_date, end_date):
    return start_date, end_date

# Finance Reconciliation -> Bookings
# Exists in ONLY corporate, parameter not needed
def get_bookings_transacted_data_query(start_date, end_date):
    return start_date, end_date
def get_bookings_recorded_data_query(start_date, end_date):
    return start_date, end_date
def get_bookings_revenue_data_query(start_date, end_date):
    return start_date, end_date
# Front-end shows "Bookings Adjusmented", past-tense for Adjustment is Adjusted
def get_bookings_adjusted_data_query(start_date, end_date):
    return start_date, end_date

# Finance Reconciliation -> Tenders, & 1 Reconciliation
# Exists in ONLY corporate, parameter not needed
def get_tender_detail_data_query(start_date, end_date):
    return start_date, end_date
def get_tender_summary_data_query(start_date, end_date):
    return start_date, end_date
def get_revenue_data_query(start_date, end_date):
    return start_date, end_date

####################################################################################

# not 100% positive which report the one below belongs to. Just keeping here for now
def get_extended_booking_data_query(start_date, end_date):
    return f"""
    WITH BookingData AS (
        SELECT
            party.createuserid,
            party.id AS partyid,
            party.rndcode AS partycode,
            party.partyname,
            party.baseagree,
            party.paid,
            party.loyalty,
            party.qty AS partyqty,
            party.totalamounts,
            party.venueid,
            party.caldate,
            FROM_UNIXTIME(party.createtstamp, '%Y-%m-%d') AS createparty,
            CONCAT('ECZ', party.ecozone) AS ecozone,
            party.currentstatus,
            party.refby,
            party.email,
            party.phone,
            party.prepaidstatus,
            party.paymentstatus,
            party.reservestatus,
            party.cancelstatus,
            party.operatestatus,
            party.totalguests AS partytotalguests,  -- Added partytotalguests here
            party.ownerids,
            party.ownerid,
            party.sourcecode,
            party.sourceloc,
            party.originatorids,
            party.comment,
            party.shift,
            party.duration,
            party.instructions,
            party.booktypes AS pbooktypes,
            party.globaltype AS pglobaltype,
            party.paytype AS ppaytype,
            GROUP_CONCAT(seat.locationid) AS locids,
            bk.subtotal,
            bk.itemname AS bitemname,
            (bk.guests * bk.qty) as itemguests,
            bk.qty AS bkqty,
            bk.booktypeid,
            bk.globaltype AS bkglobaltype,
            bk.paytype AS bkpaytype,
            bk.baseagree as value,
            bk.masteritemid,
            bk.pricing
        FROM
            BOOKING.PARTY AS party
        LEFT JOIN
            BOOKING.SEATING AS seat ON seat.partyid = party.id AND seat.status = 7
        LEFT JOIN
            BOOKING.BOOKING AS bk ON bk.partyid = party.id AND bk.status = 7
        WHERE
            party.caldate >= '{start_date}' AND 
            party.caldate <= '{end_date}' AND 
            party.status = '7' AND 
            party.cancelstatus = '' AND
            party.resellerid IN ('1927', '1017', '2064') AND
            party.venueid IN (SELECT id FROM veadb.VENUEprofile WHERE manageentid = '1927')
        GROUP BY
            bk.id, party.id
    )

    SELECT
        bd.bitemname AS "Item Name",
        COALESCE(
        (SELECT 
            CASE
                WHEN mi.itcfix IS NOT NULL AND mi.itcfix <> '' THEN CONCAT(mi.itcode, '-', mi.itcfix) 
                ELSE mi.itcode
            END
        FROM UrInventory.MASTERitem mi 
        WHERE mi.id = bd.masteritemid AND mi.status = '7' AND mi.itcode <> '0' AND mi.itcode <> ''
        LIMIT 1),
        '') AS "Item Code",
        bd.createparty AS "Created Date",
        bd.caldate AS "Event Date",
        (SELECT name FROM UrME.ECOvenues WHERE veaid = bd.venueid LIMIT 1) AS "Venue",
        bd.ecozone AS "EcoZone",
        (SELECT name FROM veadb.EVENTprofile WHERE id = (
            SELECT eventid FROM veadb.EVENTdate WHERE venueid = bd.venueid AND caldate = bd.caldate AND ecozone = bd.ecozone AND status = '7' LIMIT 1
        ) LIMIT 1) AS "Event",
        bd.partyname AS "Party Name",
        bd.currentstatus AS "Current Status",
        COALESCE(bd.shift, '') AS "Time",
        CASE
            WHEN bd.duration < 60 THEN CONCAT(bd.duration, 'm')
            WHEN bd.duration % 60 > 0 THEN CONCAT(FLOOR(bd.duration / 60), 'h', MOD(bd.duration, 60), 'm')
            ELSE CONCAT(FLOOR(bd.duration / 60), 'h')
        END AS "Duration",
        COALESCE((SELECT name FROM UrInventory.BOOKtype WHERE id = bd.booktypeid), bd.pbooktypes) AS "Book Type",
        COALESCE(bd.bkglobaltype, bd.pglobaltype) AS "Global Type",
        COALESCE(bd.bkqty, bd.partyqty) AS "Qty",
        COALESCE(bd.itemguests, bd.partytotalguests) AS "Guests",
        COALESCE(bd.bkpaytype, bd.ppaytype) AS "Pay Type",
        bd.pricing AS "Pricing",
        ROUND(bd.subtotal / 100, 2) AS "PrePay Subtotal",
        ROUND(bd.value / 100, 2) AS "Agreement",
        bd.paymentstatus AS "PrePaid Status",
        (SELECT GROUP_CONCAT(name SEPARATOR ', ') FROM UrME.LOCATION WHERE id IN (SELECT locationid FROM BOOKING.SEATING WHERE partyid = bd.partyid)) AS "Locations",
        (SELECT fullname FROM UrME.USER WHERE id = (SUBSTRING_INDEX(bd.ownerids, ',', 1))) AS "Owners",
        (SELECT fullname FROM UrME.USER WHERE id = (SUBSTRING_INDEX(bd.originatorids, ',', 1))) AS "Originators",
        (SELECT fullname FROM UrME.USER WHERE id = bd.createuserid) AS "User",
        bd.refby AS "Referred By",
        bd.sourcecode AS "Source",
        bd.email AS "Email",
        bd.phone AS "Phone",
        bd.partyid AS "Res Code",
        bd.partycode AS "Party Code",
        bd.comment AS "Comment",
        bd.instructions AS "Instruction"
    FROM
    BookingData bd
    ORDER BY
        bd.caldate, bd.venueid, bd.ecozone;
    """