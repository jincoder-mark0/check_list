from typing import Dict, Type
from core.base_parser import BaseParser

# 01_Timing_CDC
from model.parsers.timing_cdc.timing_summary_parser import TimingSummaryParser
from model.parsers.timing_cdc.setup_critical_parser import SetupCriticalParser
from model.parsers.timing_cdc.hold_critical_parser import HoldCriticalParser
from model.parsers.timing_cdc.check_timing_parser import CheckTimingParser
from model.parsers.timing_cdc.cdc_report_parser import CDCReportParser
from model.parsers.timing_cdc.cdc_critical_parser import CDCCriticalParser
from model.parsers.timing_cdc.cdc_interaction_parser import CDCInteractionParser
from model.parsers.timing_cdc.bus_skew_parser import BusSkewParser
from model.parsers.timing_cdc.clock_networks_parser import ClockNetworksParser
from model.parsers.timing_cdc.clock_utilization_parser import ClockUtilizationParser
from model.parsers.timing_cdc.pulse_width_parser import PulseWidthParser
from model.parsers.timing_cdc.timing_exceptions_parser import TimingExceptionsParser

# 02_Power_Thermal
from model.parsers.power_thermal.power_data_parser import PowerDataParser
from model.parsers.power_thermal.power_report_parser import PowerReportParser
from model.parsers.power_thermal.power_opt_parser import PowerOptParser
from model.parsers.power_thermal.ssn_report_parser import SSNReportParser
from model.parsers.power_thermal.operating_cond_parser import OperatingCondParser
from model.parsers.power_thermal.switching_activity_parser import SwitchingActivityParser

# 03_Resources_DRC
from model.parsers.resources_drc.utilization_parser import UtilizationParser
from model.parsers.resources_drc.drc_report_parser import DRCReportParser
from model.parsers.resources_drc.methodology_parser import MethodologyParser
from model.parsers.resources_drc.control_sets_parser import ControlSetsParser
from model.parsers.resources_drc.ram_utilization_parser import RAMUtilizationParser
from model.parsers.resources_drc.io_report_parser import IOReportParser
from model.parsers.resources_drc.waiver_parser import WaiverParser

# 04_Design_Analysis
from model.parsers.design_analysis.design_analysis_parser import DesignAnalysisParser
from model.parsers.design_analysis.qor_assessment_parser import QoRAssessmentParser
from model.parsers.design_analysis.qor_suggestions_parser import QoRSuggestionsParser
from model.parsers.design_analysis.pipeline_analysis_parser import PipelineAnalysisParser
from model.parsers.design_analysis.high_fanout_parser import HighFanoutParser
from model.parsers.design_analysis.debug_core_parser import DebugCoreParser

# 05_Environment_IP
from model.parsers.environment_ip.ip_status_parser import IPStatusParser
from model.parsers.environment_ip.environment_parser import EnvironmentParser
from model.parsers.environment_ip.datasheet_parser import DatasheetParser
from model.parsers.environment_ip.config_impl_parser import ConfigImplParser
from model.parsers.environment_ip.compile_order_parser import CompileOrderParser
from model.parsers.environment_ip.clocks_summary_parser import ClocksSummaryParser
from model.parsers.environment_ip.property_check_parser import PropertyCheckParser

# 06_Verification
from model.parsers.verification.coverage_report_parser import CoverageReportParser

# 07_PR_Evidence
from .pr_evidence.pr_dfx_detection_parser import PRDFXDetectionParser
from .pr_evidence.pr_na_evidence_parser import PRNAEvidenceParser
from .pr_evidence.pr_drc_report_parser import PRDRCReportParser
from .pr_evidence.pr_verify_report_parser import PRVerifyReportParser
from .pr_evidence.partial_bit_config_parser import PartialBitConfigParser
from .pr_evidence.pblock_utilization_parser import PRPBlockUtilizationParser

# 리포트 파일명(소문자)과 파서 클래스 매핑
PARSER_MAP: Dict[str, Type[BaseParser]] = {
    # 01_Timing_CDC
    "timing_summary": TimingSummaryParser,
    "setup_critical": SetupCriticalParser,
    "hold_critical": HoldCriticalParser,
    "check_timing": CheckTimingParser,
    "cdc_report": CDCReportParser,
    "cdc_critical": CDCCriticalParser,
    "cdc_interaction": CDCInteractionParser,
    "bus_skew": BusSkewParser,
    "clock_networks": ClockNetworksParser,
    "clock_utilization": ClockUtilizationParser,
    "pulse_width": PulseWidthParser,
    "timing_exceptions": TimingExceptionsParser,

    # 02_Power_Thermal
    "power_data": PowerDataParser,
    "power_report": PowerReportParser,
    "power_opt": PowerOptParser,
    "ssn_report": SSNReportParser,
    "operating_cond": OperatingCondParser,
    "switching_activity": SwitchingActivityParser,

    # 03_Resources_DRC
    "utilization": UtilizationParser,
    "drc_report": DRCReportParser,
    "methodology": MethodologyParser,
    "control_sets": ControlSetsParser,
    "ram_utilization": RAMUtilizationParser,
    "io_report": IOReportParser,
    "waiver": WaiverParser,

    # 04_Design_Analysis
    "design_analysis": DesignAnalysisParser,
    "qor_assessment": QoRAssessmentParser,
    "qor_suggestions": QoRSuggestionsParser,
    "pipeline_analysis": PipelineAnalysisParser,
    "high_fanout": HighFanoutParser,
    "debug_core": DebugCoreParser,

    # 05_Environment_IP
    "ip_status": IPStatusParser,
    "environment": EnvironmentParser,
    "datasheet": DatasheetParser,
    "config_impl": ConfigImplParser,
    "compile_order": CompileOrderParser,
    "clocks_summary": ClocksSummaryParser,
    "property_check": PropertyCheckParser,

    # 06_Verification
    "coverage_report": CoverageReportParser,

    # 07_PR_Evidence
    "pr_dfx_detection": PRDFXDetectionParser,
    "pr_na_evidence": PRNAEvidenceParser,
    "pr_drc_report": PRDRCReportParser,
    "pr_verify_report": PRVerifyReportParser,
    "partial_bit_config_summary": PartialBitConfigParser,
    "pr_pblock_utilization": PRPBlockUtilizationParser,
}
