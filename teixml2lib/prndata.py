from teixml2lib.ualog import Log

log = Log("w")
log.open("log/prndata.log", 0)

def set_log_liv(liv=1):
    log.set_liv(liv)

def prn_data(d,v=1):
    x_id = d['id']
    is_parent = d['is_parent']
    x_items = d['items']
    x_liv = d['liv']
    x_tag = d['tag']
    x_text = d['text']
    x_tail = d['tail']
    
    #c_xml_tag = x_data['c_xml_tag']
    # c_tag = x_data['c_div']
    # c_csv_tag = d['c_csv_tag']
    # c_keys = d['c_keys']
    # c_attrs = d['c_attrs']
    # c_text = d['c_text']
    # c_params = d['c_params']
    # c_parent = d['c_parent']

    t_i = d['t_i']
    t_type = d['t_type']
    t_up = d['t_up']
    t_start = d['t_start']
    t_end = d['t_end']
    t_sp = d['t_sp']
    t_ln = d['t_ln']
    t_flag = d['t_flag']
    if v==0 :
        log.log("    >> xml_data").prn()
        log.log(f"id: {x_id}").prn()
        log.log(f"is_parent: {is_parent}").prn()
        log.log(f"liv: {x_liv     }").prn()
        log.log(f"x_items: {x_items}").prn()
        log.log(f"x_tag: {x_tag}").prn()
        log.log(f"x_text: {x_text}").prn()
        log.log(f"x_tail: {x_tail}").prn()

        # log.log("    >> csv_data").prn()
        # #log.log(f"c_xml_tag: {c_xml_tag}").prn()
        # # log.log(f"c_tag: {c_tag}").prn()
        # log.log(f"c_csv_tag: {c_csv_tag}").prn()
        # log.log(f"c_keys: {c_keys}").prn()
        # log.log(f"c_attrs: {c_attrs}").prn()
        # log.log(f"c_text: {c_text}").prn()
        # log.log(f"c_params: {c_params}").prn()
        # log.log(f"c_paren: {c_parent}").prn()

        log.log("    >> t_data").prn()
        log.log(f"t_i: {t_i}").prn()
        log.log(f"t_type: {t_type}").prn()
        log.log(f"t_up: {t_up}").prn()
        log.log(f"t_start: {t_start}").prn()
        log.log(f"t_end: {t_end}").prn()
        log.log(f"t_sp: {t_sp}").prn()
        log.log(f"t_ln: {t_ln}").prn()
        log.log(f"t_flag: {t_flag}").prn()
    elif v==1:
        log.log("    >> xml_data").prn()
        log.log(f"id: {x_id}").prn()
        #log.log(f"is_parent: {is_parent}").prn()
        log.log(f"liv: {x_liv     }").prn()
        log.log(f"x_items: {x_items}").prn()
        log.log(f"x_tag: {x_tag}").prn()
        log.log(f"x_text: {x_text}").prn()
        log.log(f"x_tail: {x_tail}").prn()

        # log.log("    >> csv_data").prn()
        # log.log(f"c_csv_tag: {c_csv_tag}").prn()
        # #log.log(f"c_keys: {c_keys}").prn()
        # log.log(f"c_attrs: {c_attrs}").prn()
        # log.log(f"c_text: {c_text}").prn()
        # log.log(f"c_params: {c_params}").prn()
        # #log.log(f"c_paren: {c_parent}").prn()

        log.log("    >> t_data").prn()
        log.log(f"t_i: {t_i}").prn()
        #log.log(f"t_type: {t_type}").prn()
        log.log(f"t_up: {t_up}").prn()
        #log.log(f"t_start: {t_start}").prn()
        #log.log(f"t_end: {t_end}").prn()
        log.log(f"t_sp: {t_sp}").prn()
        #log.log(f"t_ln: {t_ln}").prn()
        log.log(f"t_flag: {t_flag}").prn()
    else:
        pass
        