from script.securityscan.scan_steps import *
target_url = "http://localhost:3000/rest/user/login"
start_zap()
visit_web()
login_web('tlqiao@thoughtworks.com', 'Qtl@com123456')
perform_spider(target_url)
get_spider_status(target_url)
perform_zap_active_scan(target_url)
get_active_scan_status(target_url)
zap_alerts_summary()
save_scan_report("/Users/taoli/report.html")
close_zap()
