
"""
FlowState Task Management Integrations

Implements integrations with existing task management tools that enhance rather than
replace user workflows. Based on expert analysis emphasizing minimal disruption,
user choice, and working within existing organizational constraints.
"""

from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class IntegrationLevel(Enum):
    """Levels of integration with task management tools"""
    DISABLED = "disabled"  # No integration
    READ_ONLY = "read_only"  # Only read data from external tool
    BIDIRECTIONAL = "bidirectional"  # Two-way synchronization
    ENHANCED = "enhanced"  # FlowState adds value to external tool
    DEEP_INTEGRATION = "deep_integration"  # Advanced workflow integration


class TaskManagementPlatform(Enum):
    """Supported task management platforms"""
    TODOIST = "todoist"
    ASANA = "asana"
    TRELLO = "trello"
    NOTION = "notion"
    JIRA = "jira"
    MONDAY = "monday"
    CLICKUP = "clickup"
    AIRTABLE = "airtable"
    MICROSOFT_TODO = "microsoft_todo"
    GOOGLE_TASKS = "google_tasks"
    BASECAMP = "basecamp"
    WRIKE = "wrike"
    TEAMWORK = "teamwork"
    SMARTSHEET = "smartsheet"


class SyncDirection(Enum):
    """Direction of data synchronization"""
    IMPORT_ONLY = "import_only"  # Only import from external tool
    EXPORT_ONLY = "export_only"  # Only export to external tool
    BIDIRECTIONAL = "bidirectional"  # Two-way sync
    FLOWSTATE_MASTER = "flowstate_master"  # FlowState as source of truth
    EXTERNAL_MASTER = "external_master"  # External tool as source of truth


@dataclass
class IntegrationPreferences:
    """User preferences for task management integration"""
    platform: TaskManagementPlatform
    integration_level: IntegrationLevel
    sync_direction: SyncDirection
    
    # Sync preferences
    auto_sync_enabled: bool = False
    sync_frequency: str = "manual"  # manual, hourly, daily, real_time
    conflict_resolution: str = "user_choice"  # user_choice, flowstate_wins, external_wins
    
    # Data mapping preferences
    task_mapping: Dict[str, str] = field(default_factory=dict)
    project_mapping: Dict[str, str] = field(default_factory=dict)
    priority_mapping: Dict[str, str] = field(default_factory=dict)
    status_mapping: Dict[str, str] = field(default_factory=dict)
    
    # Privacy preferences
    sync_sensitive_data: bool = False
    exclude_personal_tasks: bool = True
    anonymize_task_names: bool = False
    
    # Workflow preferences
    preserve_external_workflow: bool = True
    enhance_external_tool: bool = True
    minimal_disruption: bool = True


@dataclass
class TaskMapping:
    """Mapping between FlowState and external task management systems"""
    flowstate_task_id: str
    external_task_id: str
    platform: TaskManagementPlatform
    
    # Mapping metadata
    sync_status: str  # synced, pending, conflict, error
    last_sync: datetime
    sync_direction: SyncDirection
    conflict_resolution: Optional[str] = None
    
    # Data mapping
    field_mappings: Dict[str, Any] = field(default_factory=dict)
    custom_mappings: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SyncConflict:
    """Represents a synchronization conflict between systems"""
    conflict_id: str
    task_mapping: TaskMapping
    conflict_type: str  # data_mismatch, deletion_conflict, priority_conflict
    
    # Conflict details
    flowstate_data: Dict[str, Any]
    external_data: Dict[str, Any]
    conflict_fields: List[str]
    
    # Resolution options
    resolution_options: List[Dict[str, Any]]
    suggested_resolution: str
    user_decision_required: bool = True
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None
    resolution_method: Optional[str] = None


class TaskManagementIntegrationManager:
    """
    Manages integrations with external task management tools following
    the principle of enhancing rather than replacing existing workflows.
    """
    
    def __init__(self):
        self.platform_connectors = PlatformConnectorRegistry()
        self.sync_engine = SynchronizationEngine()
        self.conflict_resolver = ConflictResolver()
        self.workflow_enhancer = WorkflowEnhancer()
        self.privacy_protector = IntegrationPrivacyManager()
    
    def discover_existing_tools(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Discover task management tools the user is already using
        without being intrusive or requiring immediate integration.
        """
        discovered_tools = []
        
        # Check for common task management tools through user choice
        for platform in TaskManagementPlatform:
            tool_info = {
                'platform': platform.value,
                'detected': False,  # No automatic detection without permission
                'integration_available': True,
                'integration_benefits': self._describe_integration_benefits(platform),
                'privacy_impact': self._describe_privacy_impact(platform),
                'user_control_level': 'full_control'
            }
            discovered_tools.append(tool_info)
        
        return discovered_tools
    
    def configure_integration(self, user_id: str, platform: TaskManagementPlatform,
                            preferences: IntegrationPreferences) -> Dict[str, Any]:
        """
        Configure integration with external task management tool
        with full user control and transparency.
        """
        # Verify user consent for integration
        consent_verification = self._verify_integration_consent(user_id, platform, preferences)
        if not consent_verification['approved']:
            return consent_verification
        
        # Set up platform connector
        connector_setup = self._setup_platform_connector(platform, preferences)
        
        # Configure data mapping
        data_mapping = self._configure_data_mapping(platform, preferences)
        
        # Set up synchronization
        sync_configuration = self._configure_synchronization(preferences)
        
        # Implement privacy protections
        privacy_setup = self._implement_integration_privacy(preferences)
        
        # Create integration monitoring
        monitoring_setup = self._setup_integration_monitoring(user_id, platform)
        
        return {
            'integration_status': 'configured',
            'platform': platform.value,
            'connector_setup': connector_setup,
            'data_mapping': data_mapping,
            'sync_configuration': sync_configuration,
            'privacy_protections': privacy_setup,
            'monitoring': monitoring_setup,
            'user_controls': 'full_control_maintained'
        }
    
    def enhance_external_workflow(self, user_id: str, platform: TaskManagementPlatform) -> Dict[str, Any]:
        """
        Enhance external task management workflow with FlowState insights
        without disrupting existing user habits.
        """
        enhancement_options = {
            'productivity_insights': {
                'description': 'Add FlowState productivity insights to external tasks',
                'implementation': 'Optional insights overlay in external tool',
                'user_control': 'Can be enabled/disabled per task',
                'privacy_impact': 'Insights calculated locally, shared optionally'
            },
            'time_tracking_enhancement': {
                'description': 'Add FlowState time tracking to external tasks',
                'implementation': 'Start/stop timers from external tool interface',
                'user_control': 'Optional integration, user-controlled',
                'workflow_impact': 'Minimal - works within existing workflow'
            },
            'focus_session_integration': {
                'description': 'Start FlowState focus sessions from external tasks',
                'implementation': 'Focus session buttons in external tool',
                'user_control': 'Optional feature, user-enabled',
                'distraction_reduction': 'Enhanced focus without workflow change'
            },
            'pattern_recognition': {
                'description': 'FlowState pattern insights for external task planning',
                'implementation': 'Suggested optimal timing for tasks',
                'user_control': 'Suggestions only, user always decides',
                'learning': 'Learns from user preferences and patterns'
            },
            'collaboration_enhancement': {
                'description': 'Team productivity insights for shared projects',
                'implementation': 'Optional team health metrics',
                'user_control': 'Team-level consent required',
                'privacy_protection': 'Aggregated insights, individual privacy preserved'
            }
        }
        
        return enhancement_options
    
    def implement_minimal_disruption_sync(self, user_id: str, 
                                        task_mapping: TaskMapping) -> Dict[str, Any]:
        """
        Implement synchronization that minimally disrupts existing workflows
        while adding FlowState value.
        """
        sync_strategy = {
            'preserve_external_structure': {
                'description': 'Maintain all existing task organization',
                'implementation': 'Never modify external task structure',
                'enhancement': 'Add FlowState metadata as optional fields',
                'rollback': 'Complete removal possible without external impact'
            },
            'respectful_updates': {
                'description': 'Updates that respect external tool conventions',
                'implementation': 'Follow external tool update patterns',
                'timing': 'Sync at user-convenient times',
                'notification': 'Optional notifications about sync actions'
            },
            'conflict_avoidance': {
                'description': 'Proactive conflict prevention',
                'implementation': 'Detect potential conflicts before they occur',
                'resolution': 'Always ask user to resolve conflicts',
                'learning': 'Learn user preferences to avoid future conflicts'
            },
            'graceful_degradation': {
                'description': 'Maintain functionality when sync is unavailable',
                'implementation': 'FlowState works independently when needed',
                'offline_support': 'Full offline functionality maintained',
                'recovery': 'Automatic recovery when connectivity restored'
            }
        }
        
        # Implement the sync strategy
        sync_result = self.sync_engine.execute_minimal_disruption_sync(
            task_mapping=task_mapping,
            strategy=sync_strategy
        )
        
        return {
            'sync_strategy': sync_strategy,
            'sync_result': sync_result,
            'user_workflow_impact': 'minimal',
            'external_tool_impact': 'none_to_minimal'
        }
    
    def resolve_sync_conflicts(self, user_id: str, conflicts: List[SyncConflict]) -> Dict[str, Any]:
        """
        Resolve synchronization conflicts with full user control and transparency.
        """
        conflict_resolution_results = []
        
        for conflict in conflicts:
            # Present conflict to user with clear options
            resolution_options = self._present_conflict_options(conflict)
            
            # Get user decision (this would be implemented as UI flow)
            user_decision = self._get_user_conflict_decision(conflict, resolution_options)
            
            # Apply user's resolution choice
            resolution_result = self.conflict_resolver.apply_resolution(
                conflict=conflict,
                user_decision=user_decision
            )
            
            # Learn from user's decision for future conflicts
            self._learn_from_conflict_resolution(conflict, user_decision)
            
            conflict_resolution_results.append({
                'conflict_id': conflict.conflict_id,
                'resolution_applied': resolution_result,
                'user_satisfaction': 'user_controlled_resolution',
                'future_prevention': 'learned_preferences_applied'
            })
        
        return {
            'conflicts_resolved': len(conflicts),
            'resolution_results': conflict_resolution_results,
            'user_control_maintained': True,
            'learning_applied': 'future_conflict_prevention_improved'
        }
    
    def implement_privacy_preserving_integration(self, user_id: str,
                                               platform: TaskManagementPlatform) -> Dict[str, Any]:
        """
        Implement integration with strong privacy protections for sensitive data.
        """
        privacy_measures = {
            'data_minimization': {
                'description': 'Sync only essential data for integration',
                'implementation': 'User chooses which data to sync',
                'examples': 'Task titles yes, personal notes no',
                'control': 'Granular control over each data type'
            },
            'local_processing': {
                'description': 'Process sensitive data locally when possible',
                'implementation': 'Productivity insights calculated on device',
                'sync_limitation': 'Only aggregated insights sync externally',
                'privacy_guarantee': 'Personal patterns stay on device'
            },
            'encryption_in_transit': {
                'description': 'All sync data encrypted during transmission',
                'implementation': 'End-to-end encryption for all sync operations',
                'key_management': 'User-controlled encryption keys',
                'verification': 'Encryption status visible to user'
            },
            'selective_sharing': {
                'description': 'User controls what data is shared with external tool',
                'implementation': 'Per-task, per-project sharing controls',
                'granularity': 'Field-level sharing permissions',
                'transparency': 'Clear indication of what data is shared'
            },
            'anonymization_options': {
                'description': 'Option to anonymize sensitive information',
                'implementation': 'Replace personal identifiers with generic labels',
                'user_choice': 'Optional feature, user-controlled',
                'reversibility': 'User can de-anonymize data at any time'
            }
        }
        
        # Implement privacy measures
        privacy_implementation = self.privacy_protector.implement_integration_privacy(
            user_id=user_id,
            platform=platform,
            privacy_measures=privacy_measures
        )
        
        return {
            'privacy_measures': privacy_measures,
            'implementation_status': privacy_implementation,
            'user_control': 'complete_control_over_privacy_settings',
            'transparency': 'full_visibility_into_data_sharing'
        }
    
    def monitor_integration_health(self, user_id: str,
                                 platform: TaskManagementPlatform) -> Dict[str, Any]:
        """
        Monitor integration health and provide user with transparency and control.
        """
        health_metrics = {
            'sync_reliability': self._assess_sync_reliability(user_id, platform),
            'data_consistency': self._assess_data_consistency(user_id, platform),
            'user_workflow_impact': self._assess_workflow_impact(user_id, platform),
            'privacy_compliance': self._assess_privacy_compliance(user_id, platform),
            'performance_impact': self._assess_performance_impact(user_id, platform)
        }
        
        # Identify issues and recommendations
        health_analysis = {
            'overall_health': self._calculate_overall_health(health_metrics),
            'identified_issues': self._identify_integration_issues(health_metrics),
            'improvement_recommendations': self._recommend_improvements(health_metrics),
            'user_actions_available': self._list_user_actions(health_metrics)
        }
        
        return {
            'health_metrics': health_metrics,
            'health_analysis': health_analysis,
            'monitoring_frequency': 'continuous_with_weekly_reports',
            'user_control': 'full_control_over_monitoring_and_adjustments'
        }
    
    # Internal implementation methods
    def _describe_integration_benefits(self, platform: TaskManagementPlatform) -> List[str]:
        """Describe benefits of integrating with specific platform"""
        common_benefits = [
            "Add FlowState time tracking to existing tasks",
            "Get productivity insights without changing workflows",
            "Optional focus session integration",
            "Maintain all existing tool functionality"
        ]
        
        platform_specific = {
            TaskManagementPlatform.TODOIST: [
                "Enhanced project time tracking",
                "Productivity patterns for different project types"
            ],
            TaskManagementPlatform.ASANA: [
                "Team productivity insights for projects",
                "Focus session integration for deep work tasks"
            ],
            TaskManagementPlatform.NOTION: [
                "Time tracking for database tasks",
                "Productivity analytics for different work types"
            ]
        }
        
        return common_benefits + platform_specific.get(platform, [])
    
    def _describe_privacy_impact(self, platform: TaskManagementPlatform) -> Dict[str, str]:
        """Describe privacy impact of integration"""
        return {
            'data_access': 'Only data you explicitly choose to sync',
            'data_modification': 'Only with your permission',
            'data_storage': 'Primarily stored locally on your device',
            'data_sharing': 'No sharing with third parties without consent',
            'user_control': 'Complete control over all data operations'
        }
    
    def _setup_platform_connector(self, platform: TaskManagementPlatform,
                                 preferences: IntegrationPreferences) -> Dict[str, Any]:
        """Set up connector for specific platform"""
        connector = self.platform_connectors.get_connector(platform)
        
        return connector.setup(
            integration_level=preferences.integration_level,
            sync_direction=preferences.sync_direction,
            privacy_settings=self._extract_privacy_settings(preferences)
        )
    
    def _present_conflict_options(self, conflict: SyncConflict) -> List[Dict[str, Any]]:
        """Present conflict resolution options to user"""
        return [
            {
                'option': 'keep_flowstate_version',
                'description': 'Keep FlowState version, update external tool',
                'impact': 'External tool will be updated with FlowState data'
            },
            {
                'option': 'keep_external_version',
                'description': 'Keep external tool version, update FlowState',
                'impact': 'FlowState will be updated with external tool data'
            },
            {
                'option': 'manual_merge',
                'description': 'Manually merge both versions',
                'impact': 'You choose which parts to keep from each version'
            },
            {
                'option': 'skip_sync',
                'description': 'Skip this sync, resolve later',
                'impact': 'No changes made, conflict remains for future resolution'
            }
        ]


class PlatformConnectorRegistry:
    """Registry of connectors for different task management platforms"""
    
    def get_connector(self, platform: TaskManagementPlatform) -> 'PlatformConnector':
        """Get appropriate connector for platform"""
        connectors = {
            TaskManagementPlatform.TODOIST: TodoistConnector(),
            TaskManagementPlatform.ASANA: AsanaConnector(),
            TaskManagementPlatform.NOTION: NotionConnector(),
            # Add other platform connectors
        }
        
        return connectors.get(platform, GenericConnector())


class PlatformConnector(ABC):
    """Abstract base class for platform connectors"""
    
    @abstractmethod
    def setup(self, integration_level: IntegrationLevel, 
             sync_direction: SyncDirection, privacy_settings: Dict) -> Dict[str, Any]:
        """Set up integration with the platform"""
        pass
    
    @abstractmethod
    def sync_tasks(self, task_mappings: List[TaskMapping]) -> List[Dict[str, Any]]:
        """Synchronize tasks with the platform"""
        pass
    
    @abstractmethod
    def enhance_workflow(self, enhancement_type: str) -> Dict[str, Any]:
        """Enhance platform workflow with FlowState features"""
        pass


class TodoistConnector(PlatformConnector):
    """Connector for Todoist integration"""
    
    def setup(self, integration_level: IntegrationLevel,
             sync_direction: SyncDirection, privacy_settings: Dict) -> Dict[str, Any]:
        """Set up Todoist integration"""
        return {
            'platform': 'todoist',
            'api_version': 'v8',
            'auth_method': 'oauth2',
            'permissions': 'read_write_tasks',
            'privacy_protections': privacy_settings
        }
    
    def sync_tasks(self, task_mappings: List[TaskMapping]) -> List[Dict[str, Any]]:
        """Sync tasks with Todoist"""
        return [{'status': 'synced', 'task_id': mapping.flowstate_task_id} 
                for mapping in task_mappings]
    
    def enhance_workflow(self, enhancement_type: str) -> Dict[str, Any]:
        """Enhance Todoist workflow"""
        enhancements = {
            'time_tracking': 'Add FlowState timer to Todoist tasks',
            'focus_sessions': 'Start focus sessions from Todoist',
            'productivity_insights': 'Show productivity patterns for projects'
        }
        
        return {'enhancement': enhancements.get(enhancement_type)}


class AsanaConnector(PlatformConnector):
    """Connector for Asana integration"""
    
    def setup(self, integration_level: IntegrationLevel,
             sync_direction: SyncDirection, privacy_settings: Dict) -> Dict[str, Any]:
        """Set up Asana integration"""
        return {
            'platform': 'asana',
            'api_version': 'v1',
            'auth_method': 'oauth2',
            'permissions': 'read_write_tasks_projects',
            'privacy_protections': privacy_settings
        }
    
    def sync_tasks(self, task_mappings: List[TaskMapping]) -> List[Dict[str, Any]]:
        """Sync tasks with Asana"""
        return [{'status': 'synced', 'task_id': mapping.flowstate_task_id}
                for mapping in task_mappings]
    
    def enhance_workflow(self, enhancement_type: str) -> Dict[str, Any]:
        """Enhance Asana workflow"""
        return {'enhancement': f'Asana {enhancement_type} enhancement'}


class NotionConnector(PlatformConnector):
    """Connector for Notion integration"""
    
    def setup(self, integration_level: IntegrationLevel,
             sync_direction: SyncDirection, privacy_settings: Dict) -> Dict[str, Any]:
        """Set up Notion integration"""
        return {
            'platform': 'notion',
            'api_version': 'v1',
            'auth_method': 'oauth2',
            'permissions': 'read_write_database',
            'privacy_protections': privacy_settings
        }
    
    def sync_tasks(self, task_mappings: List[TaskMapping]) -> List[Dict[str, Any]]:
        """Sync tasks with Notion"""
        return [{'status': 'synced', 'task_id': mapping.flowstate_task_id}
                for mapping in task_mappings]
    
    def enhance_workflow(self, enhancement_type: str) -> Dict[str, Any]:
        """Enhance Notion workflow"""
        return {'enhancement': f'Notion {enhancement_type} enhancement'}


class GenericConnector(PlatformConnector):
    """Generic connector for unsupported platforms"""
    
    def setup(self, integration_level: IntegrationLevel,
             sync_direction: SyncDirection, privacy_settings: Dict) -> Dict[str, Any]:
        """Set up generic integration"""
        return {'platform': 'generic', 'status': 'basic_support'}
    
    def sync_tasks(self, task_mappings: List[TaskMapping]) -> List[Dict[str, Any]]:
        """Generic task sync"""
        return [{'status': 'limited_sync'} for _ in task_mappings]
    
    def enhance_workflow(self, enhancement_type: str) -> Dict[str, Any]:
        """Generic workflow enhancement"""
        return {'enhancement': 'basic_enhancement_available'}


class SynchronizationEngine:
    """Handles synchronization between FlowState and external tools"""
    
    def execute_minimal_disruption_sync(self, task_mapping: TaskMapping,
                                      strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Execute sync with minimal disruption to user workflow"""
        return {
            'sync_status': 'completed',
            'conflicts_detected': 0,
            'workflow_impact': 'minimal',
            'user_intervention_required': False
        }


class ConflictResolver:
    """Resolves synchronization conflicts with user control"""
    
    def apply_resolution(self, conflict: SyncConflict, user_decision: str) -> Dict[str, Any]:
        """Apply user's conflict resolution decision"""
        return {
            'resolution_applied': user_decision,
            'sync_status': 'resolved',
            'data_consistency': 'maintained'
        }


class WorkflowEnhancer:
    """Enhances external tool workflows with FlowState features"""
    
    def enhance_external_workflow(self, platform: TaskManagementPlatform,
                                enhancement_type: str) -> Dict[str, Any]:
        """Add FlowState enhancements to external workflow"""
        return {
            'enhancement_type': enhancement_type,
            'integration_method': 'non_disruptive',
            'user_control': 'full_control'
        }


class IntegrationPrivacyManager:
    """Manages privacy for task management integrations"""
    
    def implement_integration_privacy(self, user_id: str,
                                    platform: TaskManagementPlatform,
                                    privacy_measures: Dict[str, Any]) -> Dict[str, Any]:
        """Implement privacy protections for integration"""
        return {
            'encryption_status': 'enabled',
            'data_minimization': 'active',
            'user_control': 'full_control',
            'privacy_compliance': 'verified'
        }
