from typing import Dict, Type
from core.base_parser import BaseParser

from .env_parser import EnvParser
from .timing_summary_parser import TimingSummaryParser
from .utilization_parser import UtilizationParser
from .power_report_parser import PowerReportParser
from .methodology_parser import MethodologyParser
from .cdc_report_parser import CDCReportParser
from .drc_report_parser import DRCReportParser
from .ip_status_parser import IPStatusParser
from .compile_order_parser import CompileOrderParser
from .check_timing_parser import CheckTimingParser
from .clock_networks_parser import ClockNetworksParser
from .pulse_width_parser import PulseWidthParser
from .ram_utilization_parser import RAMUtilizationParser
from .io_report_parser import IOReportParser
from .clock_utilization_parser import ClockUtilizationParser
from .bus_skew_parser import BusSkewParser
from .cdc_critical_parser import CDCCriticalParser
from .cdc_interaction_parser import CDCInteractionParser
from .cdc_unsafe_parser import CDCUnsafeParser
from .clocks_summary_parser import ClocksSummaryParser
from .config_impl_parser import ConfigImplParser
from .control_sets_parser import ControlSetsParser
from .coverage_report_parser import CoverageReportParser
from .datasheet_parser import DatasheetParser
from .debug_core_parser import DebugCoreParser
from .design_analysis_parser import DesignAnalysisParser
from .high_fanout_parser import HighFanoutParser
from .hold_critical_parser import HoldCriticalParser
from .operating_cond_parser import OperatingCondParser
from .partial_bit_config_parser import PartialBitConfigParser
from .pblock_utilization_parser import PRPBlockUtilizationParser
from .pipeline_analysis_parser import PipelineAnalysisParser
from .power_opt_parser import PowerOptParser
from .pr_drc_report_parser import PRDRCReportParser
from .pr_verify_report_parser import PRVerifyReportParser
from .property_check_parser import PropertyCheckParser
from .qor_assessment_parser import QoRAssessmentParser
from .qor_suggestions_parser import QoRSuggestionsParser
from .setup_critical_parser import SetupCriticalParser
from .ssn_report_parser import SSNReportParser
from .switching_activity_parser import SwitchingActivityParser
from .timing_exceptions_parser import TimingExceptionsParser
from .waiver_parser import WaiverParser
from .pr_dfx_detection_parser import PRDFXDetectionParser
from .pr_na_evidence_parser import PRNAEvidenceParser

# 리포트 파일명(소문자)과 파서 클래스 매핑
PARSER_MAP: Dict[str, Type[BaseParser]] = {
    "environment": EnvParser,
    "timing_summary": TimingSummaryParser,
    "utilization": UtilizationParser,
    "power_report": PowerReportParser,
    "methodology": MethodologyParser,
    "cdc_report": CDCReportParser,
    "drc_report": DRCReportParser,
    "ip_status": IPStatusParser,
    "compile_order": CompileOrderParser,
    "check_timing": CheckTimingParser,
    "clock_networks": ClockNetworksParser,
    "pulse_width": PulseWidthParser,
    "ram_utilization": RAMUtilizationParser,
    "io_report": IOReportParser,
    "clock_utilization": ClockUtilizationParser,
    "bus_skew": BusSkewParser,
    "cdc_critical": CDCCriticalParser,
    "cdc_interaction": CDCInteractionParser,
    "cdc_unsafe": CDCUnsafeParser,
    "clocks_summary": ClocksSummaryParser,
    "config_impl": ConfigImplParser,
    "control_sets": ControlSetsParser,
    "coverage_report": CoverageReportParser,
    "datasheet": DatasheetParser,
    "debug_core": DebugCoreParser,
    "design_analysis": DesignAnalysisParser,
    "high_fanout": HighFanoutParser,
    "hold_critical": HoldCriticalParser,
    "operating_cond": OperatingCondParser,
    "partial_bit_config_summary": PartialBitConfigParser,
    "pr_pblock_utilization": PRPBlockUtilizationParser,
    "pipeline_analysis": PipelineAnalysisParser,
    "power_opt": PowerOptParser,
    "power_data": PowerReportParser,
    "pr_drc_report": PRDRCReportParser,
    "pr_verify_report": PRVerifyReportParser,
    "property_check": PropertyCheckParser,
    "qor_assessment": QoRAssessmentParser,
    "qor_suggestions": QoRSuggestionsParser,
    "setup_critical": SetupCriticalParser,
    "ssn_report": SSNReportParser,
    "switching_activity": SwitchingActivityParser,
    "timing_exceptions": TimingExceptionsParser,
    "waiver": WaiverParser,
    "pr_dfx_detection": PRDFXDetectionParser,
    "pr_na_evidence": PRNAEvidenceParser,
}
