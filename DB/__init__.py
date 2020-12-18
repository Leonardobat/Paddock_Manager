# -*- coding: utf-8 -*-

from multiprocessing import Pipe, Process
from .Sonoff_Discover import mDNS_S
from .IR_Discover import mDNS_IR
from .Updater_IR import list_IRDevices
from .Events_Executor import events_Executor
from .Updater_Relays import list_Sonoff
from .init_db import get_db_IR, get_db_users, get_db_relay

def optimize_db(db):
    db.execute("VACUUM")
    db.commit()
    db.close()

def init_discovery():
    optimize_db(get_db_IR())
    optimize_db(get_db_users())
    optimize_db(get_db_relay())
    updater_sonoff_conn, mDNS_S_conn = Pipe()
    updater_ir_conn, mDNS_IR_conn = Pipe()
    mdns_sonoff_process = Process(target=mDNS_S,args=(mDNS_S_conn,))
    mdns_ir_process = Process(target=mDNS_IR,args=(mDNS_IR_conn,))
    updater_sonoff_process = list_Sonoff(updater_sonoff_conn)
    updater_ir_process = list_IRDevices(updater_ir_conn)
    events_manager_process = events_Executor()
    mdns_sonoff_process.start()
    mdns_ir_process.start()
    updater_ir_process.start()
    updater_sonoff_process.start()
    events_manager_process.start()
