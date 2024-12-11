class BaseConfig:
    def __init__(self) -> None:
        self.name = self.__class__.__name__

    def __str__(self) -> str:
        return f"Config: {self.name}"

    def __repr__(self) -> str:
        return f"Config: {self.name}"


class APIM_SAP(BaseConfig):
    barrier_hierarchy_maintenance_get_barrier_hierarchies = (
        "https://gateway.api.akerbp.com/barrier-hierarchy-maintenance/v1/ZEAM_C_M_BARR_CHAR",
        "barrier-hierarchy-maintenance-get-barrier-hierarchies",
        "{baCharLvl1}-{baCharLvl2}-{baCharLvl3}-{baCharLvl4}-{baCharLvl5}",
    )
    characteristics_maintenance_characteristics = (
        "https://gateway.api.akerbp.com/characteristics-maintenance/v1/ZEAM_C_M_CHARACTERISTICS",
        "characteristics-maintenance-characteristics",
        "{characteristic}-{characteristicValue}",
    )
    functional_location_functional_location_metadata = (
        "https://gateway.api.akerbp.com/functional-location/v1/ZEAM_C_M_FLOC",
        "functional-location-functional-location-metadata",
        "{flocFunctionalLocation}",
    )
    functional_location_object_type = (
        "https://gateway.api.akerbp.com/functional-location/v1/ZEAM_C_M_CATPRO_OBJTY",
        "functional-location-object-type",
        "{objectType}",
    )
    inspectioncode_maintenance_getinspectioncodes = (
        "https://gateway.api.akerbp.com/inspection-code-maintenance/v1/ZEAM_C_M_INSPCODE",
        "inspectioncode-maintenance-getinspectioncodes",
        "{catalogProfile}-{inspectionCatalog}-{inspectionCodeGroup}-{inspectionCode}",
    )
    maintenance_plan_zeam_c_plan_floc = (
        "https://gateway.api.akerbp.com/maintenance-plan/v1/ZEAM_C_PLAN_FLOC",
        "maintenance-plan-zeam-c-plan-floc",
        "{miFunctionalLocation}-{tlUniqueActivity}",
    )
    maintenance_plan_zeam_c_plan_task = (
        "https://gateway.api.akerbp.com/maintenance-plan/v1/ZEAM_C_PLAN_TASK",
        "maintenance-plan-zeam-c-plan-task",
        "{tlUniqueActivity}-{tlGroup}-{tlOperationNode}",
    )
    maintenance_plan_zeam_c_plan_tl_bc = (
        "https://gateway.api.akerbp.com/maintenance-plan/v1/ZEAM_C_PLAN_TL_BC",
        "maintenance-plan-zeam-c-plan-tl-bc",
        "{tlUniqueActivity}-{barrierCharacteristic}",
    )
    notifications_maintenance_notifications = (
        "https://gateway.api.akerbp.com/notifications-maintenance/v1/ZEAM_C_NOTIF",
        "notifications-maintenance-notifications",
        "{notNotification}",
    )
    notifications_maintenance_notifications_long_text = (
        "https://gateway.api.akerbp.com/notifications-maintenance/v1/ZEAM_C_NOTIF_LT",
        "notifications-maintenance-notifications-long-text",
        "{notNotification}",
    )
    notifications_maintenance_notifications_rfrc_long_text = (
        "https://gateway.api.akerbp.com/notifications-maintenance/v1/ZEAM_C_NOTIF_RRC",
        "notifications-maintenance-notifications-rfrc-long-text",
        "{notNotification}-{notChangeDate}",
    )
    notifications_maintenance_notifications_repair_report = (
        "https://gateway.api.akerbp.com/notifications-maintenance/v1/ZEAM_C_NOTIF_REPAIRR",
        "notifications-maintenance-notifications-repair-report",
        "{notNotification}-{niNotificationItem}",
    )
    notifications_maintenance_notifications_repair_report_long_text = (
        "https://gateway.api.akerbp.com/notifications-maintenance/v1/ZEAM_C_NOTIF_REPAIRR_LT",
        "notifications-maintenance-notifications-repair-report-long-text",
        "{niTextName}",
    )
    planner_group_maintenance_get_planner_group = (
        "https://gateway.api.akerbp.com/planner-group-maintenance/v1/ZEAM_C_M_PLGRP",
        "planner-group-maintenance-get-planner-group",
        "{plantPlanningPlant}-{plantPlannerGroup}",
    )
    planning_plants_maintenance_ssd_codes = (
        "https://gateway.api.akerbp.com/planning-plants-maintenance/v1/ZEAM_C_M_SSDCODE",
        "planning-plants-maintenance-ssd-codes",
        "{plantPlanningPlant}-{plantSsdCode}",
    )
    planning_plants_maintenance_work_center = (
        "https://gateway.api.akerbp.com/planning-plants-maintenance/v1/ZEAM_C_M_WCTR",
        "planning-plants-maintenance-work-center",
        "{sapLanguage}-{plantPlanningPlant}-{plantWorkCenter}",
    )
    sap_barrier_area_get_barrier_hierarchies = (
        "https://gateway.api.akerbp.com/sap-barrier-area/v1/barrier-hierarchies",
        "sap-barrier-area-get-barrier-hierarchies",
        "{barrierArea}"
    )
    workorder_maintenance_pm_orders = (
        "https://gateway.api.akerbp.com/workorder-maintenance/v1/ZEAM_C_WO_V2",
        "workorder-maintenance-pm-orders",
        "{woOrder}",
    )
    workorder_maintenance_pm_orders_long_text = (
        "https://gateway.api.akerbp.com/workorder-maintenance/v1/ZEAM_C_WO_LT",
        "workorder-maintenance-pm-orders-long-text",
        "{woOrder}",
    )
    workorder_maintenance_revisions = (
        "https://gateway.api.akerbp.com/workorder-maintenance/v1/ZEAM_C_REV",
        "workorder-maintenance-revisions",
        "{revRevision}-{revPlanningPlant}",
    )
    workorderoperations_maintenance_zeam_c_wo_op_bc = (
        "https://gateway.api.akerbp.com/workorderoperations-maintenance/v1/ZEAM_C_WO_OP_BC",
        "workorderoperations-maintenance-zeam-c-wo-op-bc",
        "{opUniqueOperation}-{opBarrierCharacteristic}",
    )
    workorderoperations_maintenance_confirmations = (
        "https://gateway.api.akerbp.com/workorderoperations-maintenance/v1/ZEAM_C_WO_OP_CONF",
        "workorderoperations-maintenance-confirmations",
        "{cnfUniqueConfirmation}",
    )
    workorderoperations_maintenance_functional_location = (
        "https://gateway.api.akerbp.com/workorderoperations-maintenance/v1/ZEAM_C_WO_OP_FLOC",
        "workorderoperations-maintenance-functional-location",
        "{opUniqueOperation}-{opFunctionalLocation}",
    )
    workorderoperations_maintenance_pm_operations = (
        "https://gateway.api.akerbp.com/workorderoperations-maintenance/v1/ZEAM_C_WO_OP",
        "workorderoperations-maintenance-pm-operations",
        "{opUniqueOperation}",
    )


class PRDFIORI_SAP(BaseConfig):
    barrier_hierarchy_maintenance_get_barrier_hierarchies = (
        "https://prdfiori.akerbp.com/sap/opu/odata/sap/ZEAM_INTF_META_SRV/ZEAM_C_M_BARR_CHAR",
        "barrier-hierarchy-maintenance-get-barrier-hierarchies",
        "{baCharLvl1}-{baCharLvl2}-{baCharLvl3}-{baCharLvl4}-{baCharLvl5}",
    )
    characteristics_maintenance_characteristics = (
        "https://prdfiori.akerbp.com/sap/opu/odata/sap/ZEAM_INTF_META_SRV/ZEAM_C_M_CHARACTERISTICS",
        "characteristics-maintenance-characteristics",
        "{characteristic}-{characteristicValue}",
    )
    functional_location_functional_location_metadata = (
        "https://prdfiori.akerbp.com/sap/opu/odata/sap/ZEAM_INTF_META_SRV/ZEAM_C_M_FLOC",
        "functional-location-functional-location-metadata",
        "{flocFunctionalLocation}",
    )
    functional_location_object_type = (
        "https://prdfiori.akerbp.com/sap/opu/odata/sap/ZEAM_INTF_META_SRV/ZEAM_C_M_CATPRO_OBJTY",
        "functional-location-object-type",
        "{objectType}",
    )
    inspectioncode_maintenance_getinspectioncodes = (
        "https://prdfiori.akerbp.com/sap/opu/odata/sap/ZEAM_INTF_META_SRV/ZEAM_C_M_INSPCODE",
        "inspectioncode-maintenance-getinspectioncodes",
        "{catalogProfile}-{inspectionCatalog}-{inspectionCodeGroup}-{inspectionCode}",
    )
    maintenance_plan_zeam_c_plan_floc = (
        "https://prdfiori.akerbp.com/sap/opu/odata/sap/ZEAM_INTF_PREVM_SIM_SRV/ZEAM_C_PLAN_FLOC",
        "maintenance-plan-zeam-c-plan-floc",
        "{miFunctionalLocation}-{tlUniqueActivity}",
    )
    maintenance_plan_zeam_c_plan_task = (
        "https://prdfiori.akerbp.com/sap/opu/odata/sap/ZEAM_INTF_PREVM_SIM_SRV/ZEAM_C_PLAN_TASK",
        "maintenance-plan-zeam-c-plan-task",
        "{tlUniqueActivity}-{tlGroup}-{tlOperationNode}",
    )
    maintenance_plan_zeam_c_plan_tl_bc = (
        "https://prdfiori.akerbp.com/sap/opu/odata/sap/ZEAM_INTF_PREVM_SIM_SRV/ZEAM_C_PLAN_TL_BC",
        "maintenance-plan-zeam-c-plan-tl-bc",
        "{tlUniqueActivity}-{barrierCharacteristic}",
    )
    notifications_maintenance_notifications = (
        "https://prdfiori.akerbp.com/sap/opu/odata/sap/ZEAM_INTF_WONOT_SRV/ZEAM_C_NOTIF",
        "notifications-maintenance-notifications",
        "{notNotification}",
    )
    notifications_maintenance_notifications_long_text = (
        "https://prdfiori.akerbp.com/sap/opu/odata/sap/ZEAM_INTF_WONOT_SRV/ZEAM_C_NOTIF_LT",
        "notifications-maintenance-notifications-long-text",
        "{notNotification}",
    )
    notifications_maintenance_notifications_rfrc_long_text = (
        "https://prdfiori.akerbp.com/sap/opu/odata/sap/ZEAM_INTF_WONOT_SRV/ZEAM_C_NOTIF_RRC",
        "notifications-maintenance-notifications-rfrc-long-text",
        "{notNotification}-{notChangeDate}",
    )
    notifications_maintenance_notifications_repair_report = (
        "https://prdfiori.akerbp.com/sap/opu/odata/sap/ZEAM_INTF_WONOT_SRV/ZEAM_C_NOTIF_REPAIRR",
        "notifications-maintenance-notifications-repair-report",
        "{notNotification}-{niNotificationItem}",
    )
    notifications_maintenance_notifications_repair_report_long_text = (
        "https://prdfiori.akerbp.com/sap/opu/odata/sap/ZEAM_INTF_WONOT_SRV/ZEAM_C_NOTIF_REPAIRR_LT",
        "notifications-maintenance-notifications-repair-report-long-text",
        "{niTextName}",
    )
    planner_group_maintenance_get_planner_group = (
        "https://prdfiori.akerbp.com/sap/opu/odata/sap/ZEAM_INTF_META_SRV/ZEAM_C_M_PLGRP",
        "planner-group-maintenance-get-planner-group",
        "{plantPlanningPlant}-{plantPlannerGroup}",
    )
    planning_plants_maintenance_ssd_codes = (
        "https://prdfiori.akerbp.com/sap/opu/odata/sap/ZEAM_INTF_META_SRV/ZEAM_C_M_SSDCODE",
        "planning-plants-maintenance-ssd-codes",
        "{plantPlanningPlant}-{plantSsdCode}",
    )
    planning_plants_maintenance_work_center = (
        "https://prdfiori.akerbp.com/sap/opu/odata/sap/ZEAM_INTF_META_SRV/ZEAM_C_M_WCTR",
        "planning-plants-maintenance-work-center",
        "{sapLanguage}-{plantPlanningPlant}-{plantWorkCenter}",
    )
    sap_barrier_area_get_barrier_hierarchies = (
        "https://prdfiori.akerbp.com/sap/opu/odata/sap/ZEAM_INTF_META_SRV/zeam_c_m_barrierarea",
        "sap-barrier-area-get-barrier-hierarchies",
        "{barrierArea}"
    )
    workorder_maintenance_pm_orders = (
        "https://prdfiori.akerbp.com/sap/opu/odata/sap/ZEAM_INTF_WONOT_SRV/ZEAM_C_WO_V2",
        "workorder-maintenance-pm-orders",
        "{woOrder}",
    )
    workorder_maintenance_pm_orders_long_text = (
        "https://prdfiori.akerbp.com/sap/opu/odata/sap/ZEAM_INTF_WONOT_SRV/ZEAM_C_WO_LT",
        "workorder-maintenance-pm-orders-long-text",
        "{woOrder}",
    )
    workorder_maintenance_revisions = (
        "https://prdfiori.akerbp.com/sap/opu/odata/sap/ZEAM_INTF_WONOT_SRV/ZEAM_C_REV",
        "workorder-maintenance-revisions",
        "{revRevision}-{revPlanningPlant}",
    )
    workorderoperations_maintenance_zeam_c_wo_op_bc = (
        "https://prdfiori.akerbp.com/sap/opu/odata/sap/ZEAM_INTF_WONOT_SRV/ZEAM_C_WO_OP_BC",
        "workorderoperations-maintenance-zeam-c-wo-op-bc",
        "{opUniqueOperation}-{opBarrierCharacteristic}",
    )
    workorderoperations_maintenance_confirmations = (
        "https://prdfiori.akerbp.com/sap/opu/odata/sap/ZEAM_INTF_WONOT_SRV/ZEAM_C_WO_OP_CONF",
        "workorderoperations-maintenance-confirmations",
        "{cnfUniqueConfirmation}",
    )
    workorderoperations_maintenance_functional_location = (
        "https://prdfiori.akerbp.com/sap/opu/odata/sap/ZEAM_INTF_WONOT_SRV/ZEAM_C_WO_OP_FLOC",
        "workorderoperations-maintenance-functional-location",
        "{opUniqueOperation}-{opFunctionalLocation}",
    )
    workorderoperations_maintenance_pm_operations = (
        "https://prdfiori.akerbp.com/sap/opu/odata/sap/ZEAM_INTF_WONOT_SRV/ZEAM_C_WO_OP",
        "workorderoperations-maintenance-pm-operations",
        "{opUniqueOperation}",
    )


class CDF_SAP(BaseConfig):
    barrier_hierarchy_maintenance_get_barrier_hierarchies = (
        "raw_apim-sap",
        "barrier-hierarchy-maintenance-get-barrier-hierarchies",
        "{baCharLvl1}-{baCharLvl2}-{baCharLvl3}-{baCharLvl4}-{baCharLvl5}",
    )
    characteristics_maintenance_characteristics = (
        "raw_apim-sap",
        "characteristics-maintenance-characteristics",
        "{characteristic}-{characteristicValue}",
    )
    functional_location_functional_location_metadata = (
        "raw_apim-sap",
        "functional-location-functional-location-metadata",
        "{flocFunctionalLocation}",
    )
    functional_location_object_type = (
        "raw_apim-sap",
        "functional-location-object-type",
        "{objectType}",
    )
    inspectioncode_maintenance_getinspectioncodes = (
        "raw_apim-sap",
        "inspectioncode-maintenance-getinspectioncodes",
        "{catalogProfile}-{inspectionCatalog}-{inspectionCodeGroup}-{inspectionCode}",
    )
    maintenance_plan_zeam_c_plan_floc = (
        "raw_apim-sap",
        "maintenance-plan-zeam-c-plan-floc",
        "{miFunctionalLocation}-{tlUniqueActivity}",
    )
    maintenance_plan_zeam_c_plan_task = (
        "raw_apim-sap",
        "maintenance-plan-zeam-c-plan-task",
        "{tlUniqueActivity}-{tlGroup}-{tlOperationNode}",
    )
    maintenance_plan_zeam_c_plan_tl_bc = (
        "raw_apim-sap",
        "maintenance-plan-zeam-c-plan-tl-bc",
        "{tlUniqueActivity}-{barrierCharacteristic}",
    )
    notifications_maintenance_notifications = (
        "raw_apim-sap",
        "notifications-maintenance-notifications",
        "{notNotification}",
    )
    notifications_maintenance_notifications_long_text = (
        "raw_apim-sap",
        "notifications-maintenance-notifications-long-text",
        "{notNotification}",
    )
    notifications_maintenance_notifications_rfrc_long_text = (
        "raw_apim-sap",
        "notifications-maintenance-notifications-rfrc-long-text",
        "{notNotification}-{notChangeDate}",
    )
    notifications_maintenance_notifications_repair_report = (
        "raw_apim-sap",
        "notifications-maintenance-notifications-repair-report",
        "{notNotification}-{niNotificationItem}",
    )
    notifications_maintenance_notifications_repair_report_long_text = (
        "raw_apim-sap",
        "notifications-maintenance-notifications-repair-report-long-text",
        "{niTextName}",
    )
    planner_group_maintenance_get_planner_group = (
        "raw_apim-sap",
        "planner-group-maintenance-get-planner-group",
        "{plantPlanningPlant}-{plantPlannerGroup}",
    )
    planning_plants_maintenance_ssd_codes = (
        "raw_apim-sap",
        "planning-plants-maintenance-ssd-codes",
        "{plantPlanningPlant}-{plantSsdCode}",
    )
    planning_plants_maintenance_work_center = (
        "raw_apim-sap",
        "planning-plants-maintenance-work-center",
        "{sapLanguage}-{plantPlanningPlant}-{plantWorkCenter}",
    )
    sap_barrier_area_get_barrier_hierarchies = (
        "raw_apim-sap",
        "sap-barrier-area-get-barrier-hierarchies",
        "{barrierArea}",
    )
    workorder_maintenance_pm_orders = (
        "raw_apim-sap",
        "workorder-maintenance-pm-orders",
        "{woOrder}",
    )
    workorder_maintenance_pm_orders_long_text = (
        "raw_apim-sap",
        "workorder-maintenance-pm-orders-long-text",
        "{woOrder}",
    )
    workorder_maintenance_revisions = (
        "raw_apim-sap",
        "workorder-maintenance-revisions",
        "{revRevision}-{revPlanningPlant}",
    )
    workorderoperations_maintenance_zeam_c_wo_op_bc = (
        "raw_apim-sap",
        "workorderoperations-maintenance-zeam-c-wo-op-bc",
        "{opUniqueOperation}-{opBarrierCharacteristic}",
    )
    workorderoperations_maintenance_confirmations = (
        "raw_apim-sap",
        "workorderoperations-maintenance-confirmations",
        "{cnfUniqueConfirmation}",
    )
    workorderoperations_maintenance_functional_location = (
        "raw_apim-sap",
        "workorderoperations-maintenance-functional-location",
        "{opUniqueOperation}-{opFunctionalLocation}",
    )
    workorderoperations_maintenance_pm_operations = (
        "raw_apim-sap",
        "workorderoperations-maintenance-pm-operations",
        "{opUniqueOperation}",
    )


class CDF_SAP_GOOGLE(BaseConfig):
    barrier_hierarchy_maintenance_get_barrier_hierarchies = (
        "e2e-maintenance-sap",
        "barrier-hierarchy-maintenance-get-barrier-hierarchies",
        "{baCharLvl1}-{baCharLvl2}-{baCharLvl3}-{baCharLvl4}-{baCharLvl5}",
    )
    characteristics_maintenance_characteristics = (
        "e2e-maintenance-sap",
        "characteristics-maintenance-characteristics",
        "{characteristic}-{characteristicValue}",
    )
    functional_location_functional_location_metadata = (
        "e2e-maintenance-sap",
        "functional-location-functional-location-metadata",
        "{flocFunctionalLocation}",
    )
    functional_location_object_type = (
        "e2e-maintenance-sap",
        "functional-location-object-type",
        "{objectType}",
    )
    inspectioncode_maintenance_getinspectioncodes = (
        "e2e-maintenance-sap",
        "inspectioncode-maintenance-getinspectioncodes",
        "{catalogProfile}-{inspectionCatalog}-{inspectionCodeGroup}-{inspectionCode}",
    )
    maintenance_plan_zeam_c_plan_floc = (
        "e2e-maintenance-sap",
        "maintenance-plan-zeam-c-plan-floc",
        "{miFunctionalLocation}-{tlUniqueActivity}",
    )
    maintenance_plan_zeam_c_plan_task = (
        "e2e-maintenance-sap",
        "maintenance-plan-zeam-c-plan-task",
        "{tlUniqueActivity}-{tlGroup}-{tlOperationNode}",
    )
    maintenance_plan_zeam_c_plan_tl_bc = (
        "e2e-maintenance-sap",
        "maintenance-plan-zeam-c-plan-tl-bc",
        "{tlUniqueActivity}-{barrierCharacteristic}",
    )
    notifications_maintenance_notifications = (
        "e2e-maintenance-sap",
        "notifications-maintenance-notifications",
        "{notNotification}",
    )
    notifications_maintenance_notifications_long_text = (
        "e2e-maintenance-sap",
        "notifications-maintenance-notifications-long-text",
        "{notNotification}",
    )
    notifications_maintenance_notifications_rfrc_long_text = (
        "e2e-maintenance-sap",
        "notifications-maintenance-notifications-rfrc-long-text",
        "{notNotification}-{notChangeDate}",
    )
    notifications_maintenance_notifications_repair_report = (
        "e2e-maintenance-sap",
        "notifications-maintenance-notifications-repair-report",
        "{notNotification}-{niNotificationItem}",
    )
    notifications_maintenance_notifications_repair_report_long_text = (
        "e2e-maintenance-sap",
        "notifications-maintenance-notifications-repair-report-long-text",
        "{niTextName}",
    )
    planner_group_maintenance_get_planner_group = (
        "e2e-maintenance-sap",
        "planner-group-maintenance-get-planner-group",
        "{plantPlanningPlant}-{plantPlannerGroup}",
    )
    planning_plants_maintenance_ssd_codes = (
        "e2e-maintenance-sap",
        "planning-plants-maintenance-ssd-codes",
        "{plantPlanningPlant}-{plantSsdCode}",
    )
    planning_plants_maintenance_work_center = (
        "e2e-maintenance-sap",
        "planning-plants-maintenance-work-center",
        "{sapLanguage}-{plantPlanningPlant}-{plantWorkCenter}",
    )
    sap_barrier_area_get_barrier_hierarchies = (
        "e2e-maintenance-sap",
        "sap-barrier-area-get-barrier-hierarchies",
        "{barrierArea}",
    )
    workorder_maintenance_pm_orders = (
        "e2e-maintenance-sap",
        "workorder-maintenance-pm-orders",
        "{woOrder}",
    )
    workorder_maintenance_pm_orders_long_text = (
        "e2e-maintenance-sap",
        "workorder-maintenance-pm-orders-long-text",
        "{woOrder}",
    )
    workorder_maintenance_revisions = (
        "e2e-maintenance-sap",
        "workorder-maintenance-revisions",
        "{revRevision}-{revPlanningPlant}",
    )
    workorderoperations_maintenance_zeam_c_wo_op_bc = (
        "e2e-maintenance-sap",
        "workorderoperations-maintenance-zeam-c-wo-op-bc",
        "{opUniqueOperation}-{opBarrierCharacteristic}",
    )
    workorderoperations_maintenance_confirmations = (
        "e2e-maintenance-sap",
        "workorderoperations-maintenance-confirmations",
        "{cnfUniqueConfirmation}",
    )
    workorderoperations_maintenance_functional_location = (
        "e2e-maintenance-sap",
        "workorderoperations-maintenance-functional-location",
        "{opUniqueOperation}-{opFunctionalLocation}",
    )
    workorderoperations_maintenance_pm_operations = (
        "e2e-maintenance-sap",
        "workorderoperations-maintenance-pm-operations",
        "{opUniqueOperation}",
    )


class DEVOPS_SAP(BaseConfig):
    barrier_hierarchy_maintenance_get_barrier_hierarchies = (
        "API_BarrierHierarchy_Maintenance",
        "GetBarrierHierarchiesResponseCode200",
    )
    characteristics_maintenance_characteristics = (
        "API_Characteristics_Maintenance",
        "GetCharacteristicsResponseCode200",
    )
    functional_location_functional_location_metadata = (
        "API_FunctionalLocation",
        "GetFunctionalLocationMetadata",
    )
    functional_location_object_type = (
        "API_FunctionalLocation",
        "GetObjectTypeResponseCode200",
    )
    inspectioncode_maintenance_getinspectioncodes = (
        "API_InspCode_Maintenance",
        "GetInspectionCodesResponseCode200",
    )
    maintenance_plan_zeam_c_plan_task = (
        "API_MaintenancePlan",
        "GetMaintenancePlanTaskResponseCode200",
    )
    notifications_maintenance_notifications = (
        "API_Notifications_Maintenance",
        "GetNotificationsResponseCode200",
    )
    notifications_maintenance_notifications_long_text = (
        "API_Notifications_Maintenance",
        "GetNotificationsLongTextResponseCode200",
    )
    notifications_maintenance_notifications_rfrc_long_text = (
        "API_Notifications_Maintenance",
        "GetNotificationsReasonForRejectCancelResponseCode200",
    )
    notifications_maintenance_notifications_repair_report = (
        "API_Notifications_Maintenance",
        "GetNotificationsRepairReportResponseCode200",
    )
    notifications_maintenance_notifications_repair_report_long_text = (
        "API_Notifications_Maintenance",
        "GetNotificationsRepairReportLongTextResponseCode200",
    )
    planner_group_maintenance_get_planner_group = (
        "API_PlannerGroup",
        "GetPlannerGroupResponseCode200",
    )
    planning_plants_maintenance_ssd_codes = (
        "API_Planning_Plants_Maintenance",
        "GetSSDCodesResponseCode200",
    )
    planning_plants_maintenance_work_center = (
        "API_Planning_Plants_Maintenance",
        "GetWorkCenterResponseCode200",
    )
    sap_barrier_area_get_barrier_hierarchies = (
        "API_SAP_Barrier_Area",
        "GetBarrierHierarchiesResponseCode200",
    )
    workorder_maintenance_pm_orders = (
        "API_Workorder_Maintenance",
        "GetPMOrdersResponseCode200",
    )
    workorder_maintenance_pm_orders_long_text = (
        "API_Workorder_Maintenance",
        "GetPMOrdersLongTextResponseCode200",
    )
    workorder_maintenance_revisions = (
        "API_Workorder_Maintenance",
        "GetRevisionsResponseCode200",
    )
    workorderoperations_maintenance_zeam_c_wo_op_bc = (
        "API_WorkOrderOperations_Maintenance",
        "GetWOBarrierResponseCode200",
    )
    workorderoperations_maintenance_confirmations = (
        "API_WorkOrderOperations_Maintenance",
        "GetConfirmationsResponseCode200",
    )
    workorderoperations_maintenance_functional_location = (
        "API_WorkOrderOperations_Maintenance",
        "GetFunctionalLocationResponseCode200",
    )
    workorderoperations_maintenance_pm_operations = (
        "API_WorkOrderOperations_Maintenance",
        "GetPMOperationsResponseCode200",
    )


class APIM_PIMS(BaseConfig):
    bm_findings = (
        "https://gateway.api.akerbp.com/pims/v1/operations/bmfindings",
        "bm-findings",
        "{FindingNo}-{Created}",
    )
    fsa_findings = (
        "https://gateway.api.akerbp.com/pims/v1/quality/fsa-findings_int_ops",
        "fsa-findings",
        "{FindingNo}-{Created}",
    )
    hazop_findings = (
        "https://gateway.api.akerbp.com/pims/v1/quality/hazopfindings",
        "hazop-findings",
        "{FindingNo}-{Created}",
    )


class CDF_PIMS(BaseConfig):
    bm_findings = (
        "raw_apim-pims",
        "bm-findings",
        "{FindingNo}-{Created}",
    )
    fsa_findings = (
        "raw_apim-pims",
        "fsa-findings",
        "{FindingNo}-{Created}",
    )
    hazop_findings = (
        "raw_apim-pims",
        "hazop-findings",
        "{FindingNo}-{Created}",
    )


class CDF_PIMS_GOOGLE(BaseConfig):
    bm_findings = (
        "e2e-maintenance-pims",
        "bm-findings",
        "{FindingNo}-{Created}",
    )
    fsa_findings = (
        "e2e-maintenance-pims",
        "fsa-findings",
        "{FindingNo}-{Created}",
    )
    hazop_findings = (
        "e2e-maintenance-pims",
        "hazop-findings",
        "{FindingNo}-{Created}",
    )


class APIM_WIMS(BaseConfig):
    well_test_results_testresults_intervals = (
        "https://gateway.api.akerbp.com/welltestresults/v1/TestResults/intervals",
        "well-test-results-testresults-intervals",
        "{id}"
    )

    well_integrity_summary = (
        "https://gateway.api.akerbp.com/wellintegrity/v1/Integrity/summary",
        "well integrity summary",
        "{id}"

    )


class CDF_WIMS(BaseConfig):
    well_test_results_testresults_intervals = (
        "raw_apim-wims",
        "well-test-results-testresults-intervals",
        "{id}"
    )

    well_integrity_summary = (
        "raw_apim-wims",
        "well integrity summary",
        "{id}"

    )


class CDF_WIMS_GOOGLE(BaseConfig):
    well_test_results_testresults_intervals = (
        "e2e-maintenance-wims",
        "well-test-results-testresults-intervals",
        "{id}"
    )

    well_integrity_summary = (
        "e2e-maintenance-wims",
        "well integrity summary",
        "{id}"

    )


class CDF_SYNERGI(BaseConfig):
    action_status = (
        "raw_dwh-synergi",
        "ActionStatus",
        "{ActionStatus_Id}_{Language_Id}",
    )
    action_transaction = (
        "raw_dwh-synergi",
        "ActionTransaction",
        "{ActionTransactions_Id}",
    )
    application = (
        "raw_dwh-synergi",
        "Application",
        "{Application_Id}_{Language_Id}",
    )
    asset = (
        "raw_dwh-synergi",
        "Asset",
        "{Asset_Id}",
    )
    audittype = (
        "raw_dwh-synergi",
        "AuditType",
        "{AuditType_Id}_{Language_Id}",
    )
    consequence = (
        "raw_dwh-synergi",
        "Consequence",
        "{Consequence_Id}_{ConsequenceCategory}_{Language_Id}",
    )
    location = (
        "raw_dwh-synergi",
        "Location",
        "{Location_Id}_{Language_Id}",
    )
    reference = (
        "raw_dwh-synergi",
        "Reference",
        "{Reference_Id}_{Language_Id}",
    )
    status = (
        "raw_dwh-synergi",
        "Status",
        "{Status_Id}_{Language_Id}",
    )
    synergi_and_transaction = (
        "raw_dwh-synergi",
        "SynergiAndTransaction",
        "{Synergi_Id}",
    )
    synergi_reference = (
        "raw_dwh-synergi",
        "SynergiReference",
        "{Synergi_Id}_{Reference_Id}_{REFERENCE_NO}_{ESDPSD}_{PERSONAL_INJURY}_{SPILL}",
    )
    unit = (
        "raw_dwh-synergi",
        "Unit",
        "{Unit_Id}_{Language_Id}",
    )


class CDF_SYNERGI_GOOGLE(BaseConfig):
    action_status = (
        "synergi",
        "ActionStatus",
        "{ActionStatus_Id}_{Language_Id}",
    )
    action_transaction = (
        "synergi",
        "ActionTransaction",
        "{ActionTransactions_Id}",
    )
    application = (
        "synergi",
        "Application",
        "{Application_Id}_{Language_Id}",
    )
    asset = (
        "synergi",
        "Asset",
        "{Asset_Id}",
    )
    audittype = (
        "synergi",
        "AuditType",
        "{AuditType_Id}_{Language_Id}",
    )
    consequence = (
        "synergi",
        "Consequence",
        "{Consequence_Id}_{ConsequenceCategory}_{Language_Id}",
    )
    location = (
        "synergi",
        "Location",
        "{Location_Id}_{Language_Id}",
    )
    reference = (
        "synergi",
        "Reference",
        "{Reference_Id}_{Language_Id}",
    )
    status = (
        "synergi",
        "Status",
        "{Status_Id}_{Language_Id}",
    )
    synergi_and_transaction = (
        "synergi",
        "SynergiAndTransaction",
        "{Synergi_Id}",
    )
    synergi_reference = (
        "synergi",
        "SynergiReference",
        "{Synergi_Id}_{Reference_Id}_{REFERENCE_NO}_{ESDPSD}_{PERSONAL_INJURY}_{SPILL}",
    )
    unit = (
        "synergi",
        "Unit",
        "{Unit_Id}_{Language_Id}",
    )


class CDF_AIM(BaseConfig):
    aim_anomaly = (
        "raw_dwh_aim_anomaly",
        "aim_anomaly",
        "{ANOMALY_RECORD_NUMBER}",
    )
    aim_anomaly_delete_list = (
        "raw_dwh_aim_anomaly",
        "aim_anomaly_delete_list",
        "{externalId}",
    )


class CDF_AIM_GOOGLE(BaseConfig):
    aim_anomaly = (
        "dwh_aim_anomaly",
        "aim_anomaly",
        "{ANOMALY_RECORD_NUMBER}",
    )
    aim_anomaly_delete_list = (
        "dwh_aim_anomaly",
        "aim_anomaly_delete_list",
        "{externalId}",
    )


class CDF_OSM(BaseConfig):
    v_isolation = (
        "raw_dwh-osm",
        "v_isolation",
        "{V_ISOLATION_Id}",
    )
    v_isolationlist = (
        "raw_dwh-osm",
        "v_isolationlist",
        "{V_ISOLATIONLIST_Id}",
    )
    v_isolationlisttag = (
        "raw_dwh-osm",
        "v_isolationlisttag",
        "{V_ISOLATIONLISTTAG_Id}",
    )
    v_isolationlistworkpermit = (
        "raw_dwh-osm",
        "v_isolationlistworkpermit",
        "{V_ISOLATIONLISTWORKPERMIT_Id}",
    )
    v_isolationpoint = (
        "raw_dwh-osm",
        "v_isolationpoint",
        "{V_ISOLATIONPOINT_Id}",
    )
    v_isolationtag = (
        "raw_dwh-osm",
        "v_isolationtag",
        "{V_ISOLATIONTAG_Id}",
    )
    v_isolationworkorder = (
        "raw_dwh-osm",
        "v_isolationworkorder",
        "{V_ISOLATIONWORKORDER_Id}",
    )
    v_safejobanalysis = (
        "raw_dwh-osm",
        "v_safejobanalysis",
        "{V_SAFEJOBANALYSIS_Id}",
    )
    v_workorder = (
        "raw_dwh-osm",
        "v_workorder",
        "{V_WORKORDER_Id}",
    )
    v_workpermit = (
        "raw_dwh-osm",
        "v_workpermit",
        "{V_WORKPERMIT_Id}",
    )
    v_workpermitsja = (
        "raw_dwh-osm",
        "v_workpermitsja",
        "{V_WORKPERMITSJA_Id}",
    )


class CDF_OSM_GOOGLE(BaseConfig):
    v_isolation = (
        "osm",
        "v_isolation",
        "{V_ISOLATION_Id}",
    )
    v_isolationlist = (
        "osm",
        "v_isolationlist",
        "{V_ISOLATIONLIST_Id}",
    )
    v_isolationlisttag = (
        "osm",
        "v_isolationlisttag",
        "{V_ISOLATIONLISTTAG_Id}",
    )
    v_isolationlistworkpermit = (
        "osm",
        "v_isolationlistworkpermit",
        "{V_ISOLATIONLISTWORKPERMIT_Id}",
    )
    v_isolationpoint = (
        "osm",
        "v_isolationpoint",
        "{V_ISOLATIONPOINT_Id}",
    )
    v_isolationtag = (
        "osm",
        "v_isolationtag",
        "{V_ISOLATIONTAG_Id}",
    )
    v_isolationworkorder = (
        "osm",
        "v_isolationworkorder",
        "{V_ISOLATIONWORKORDER_Id}",
    )
    v_safejobanalysis = (
        "osm",
        "v_safejobanalysis",
        "{V_SAFEJOBANALYSIS_Id}",
    )
    v_workorder = (
        "osm",
        "v_workorder",
        "{V_WORKORDER_Id}",
    )
    v_workpermit = (
        "osm",
        "v_workpermit",
        "{V_WORKPERMIT_Id}",
    )
    v_workpermitsja = (
        "osm",
        "v_workpermitsja",
        "{V_WORKPERMITSJA_Id}",
    )


