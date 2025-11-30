"""
Observability Module - Logging, Tracing, and Metrics

This demonstrates observability features for the agent system
"""

import logging
import sys
from datetime import datetime
from typing import Dict, Any, List
import json

# Global activity log for tracking all agent activities
ACTIVITY_LOG: List[Dict[str, Any]] = []

# Global metrics storage
METRICS: Dict[str, Any] = {
    'total_requests': 0,
    'successful_requests': 0,
    'failed_requests': 0,
    'agent_execution_times': {},
    'tool_usage_count': {},
    'errors': []
}

def setup_logging(log_level: int = logging.INFO) -> logging.Logger:
   
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Remove existing handlers
    logger.handlers = []
    
    # Create console handler with formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    # Optional: File handler for persistent logs
    try:
        file_handler = logging.FileHandler('investment_agent.log')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Could not create file handler: {e}")
    
    logger.info("Logging system initialized")
    
    return logger

def log_agent_activity(
    agent_name: str,
    activity: str,
    session_id: str,
    metadata: Dict[str, Any] = None
) -> None:
   
    activity_entry = {
        'timestamp': datetime.now().isoformat(),
        'agent_name': agent_name,
        'activity': activity,
        'session_id': session_id,
        'metadata': metadata or {}
    }
    
    ACTIVITY_LOG.append(activity_entry)
    
    # Also log to standard logging
    logger = logging.getLogger(agent_name)
    logger.info(f"[{session_id}] {activity}")

def get_activity_log(
    session_id: str = None,
    agent_name: str = None
) -> List[Dict[str, Any]]:
 
    filtered_log = ACTIVITY_LOG
    
    if session_id:
        filtered_log = [
            entry for entry in filtered_log
            if entry['session_id'] == session_id
        ]
    
    if agent_name:
        filtered_log = [
            entry for entry in filtered_log
            if entry['agent_name'] == agent_name
        ]
    
    return filtered_log

def record_metric(metric_name: str, value: Any) -> None:
    
    if metric_name not in METRICS:
        METRICS[metric_name] = []
    
    metric_entry = {
        'timestamp': datetime.now().isoformat(),
        'value': value
    }
    
    if isinstance(METRICS[metric_name], list):
        METRICS[metric_name].append(metric_entry)
    else:
        METRICS[metric_name] = value
    
    logger = logging.getLogger('Metrics')
    logger.debug(f"Recorded metric: {metric_name} = {value}")

def increment_metric(metric_name: str, amount: int = 1) -> None:
    
    if metric_name not in METRICS:
        METRICS[metric_name] = 0
    
    METRICS[metric_name] += amount

def record_agent_execution_time(
    agent_name: str,
    execution_time_seconds: float
) -> None:
 
    if agent_name not in METRICS['agent_execution_times']:
        METRICS['agent_execution_times'][agent_name] = []
    
    METRICS['agent_execution_times'][agent_name].append({
        'timestamp': datetime.now().isoformat(),
        'execution_time': execution_time_seconds
    })
    
    logger = logging.getLogger('Metrics')
    logger.info(f"{agent_name} execution time: {execution_time_seconds:.2f}s")

def record_tool_usage(tool_name: str) -> None:
    
    if tool_name not in METRICS['tool_usage_count']:
        METRICS['tool_usage_count'][tool_name] = 0
    
    METRICS['tool_usage_count'][tool_name] += 1

def record_error(
    error_type: str,
    error_message: str,
    context: Dict[str, Any] = None
) -> None:
   
    error_entry = {
        'timestamp': datetime.now().isoformat(),
        'error_type': error_type,
        'error_message': error_message,
        'context': context or {}
    }
    
    METRICS['errors'].append(error_entry)
    
    logger = logging.getLogger('Errors')
    logger.error(f"{error_type}: {error_message}")

def get_metrics_summary() -> Dict[str, Any]:
   
    summary = {
        'total_requests': METRICS.get('total_requests', 0),
        'successful_requests': METRICS.get('successful_requests', 0),
        'failed_requests': METRICS.get('failed_requests', 0),
        'success_rate': 0,
        'tool_usage': METRICS.get('tool_usage_count', {}),
        'total_errors': len(METRICS.get('errors', [])),
        'agent_performance': {}
    }
    
    # Calculate success rate
    total = summary['total_requests']
    if total > 0:
        summary['success_rate'] = (summary['successful_requests'] / total) * 100
    
    # Calculate average execution times per agent
    for agent_name, times in METRICS.get('agent_execution_times', {}).items():
        if times:
            avg_time = sum(t['execution_time'] for t in times) / len(times)
            summary['agent_performance'][agent_name] = {
                'average_execution_time': round(avg_time, 2),
                'total_executions': len(times)
            }
    
    return summary

def export_observability_data(filename: str) -> bool:
    
    try:
        export_data = {
            'activity_log': ACTIVITY_LOG,
            'metrics': METRICS,
            'metrics_summary': get_metrics_summary(),
            'exported_at': datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        logger = logging.getLogger('Observability')
        logger.info(f"Exported observability data to {filename}")
        
        return True
        
    except Exception as e:
        logger = logging.getLogger('Observability')
        logger.error(f"Failed to export observability data: {str(e)}")
        return False

def print_metrics_report() -> None:
    
    summary = get_metrics_summary()
    
    print("\n" + "=" * 80)
    print("OBSERVABILITY METRICS REPORT")
    print("=" * 80)
    print(f"\nTotal Requests: {summary['total_requests']}")
    print(f"Successful: {summary['successful_requests']}")
    print(f"Failed: {summary['failed_requests']}")
    print(f"Success Rate: {summary['success_rate']:.2f}%")
    
    print("\nTool Usage:")
    for tool, count in summary['tool_usage'].items():
        print(f"  - {tool}: {count} times")
    
    print("\nAgent Performance:")
    for agent, perf in summary['agent_performance'].items():
        print(f"  - {agent}:")
        print(f"    Average Execution Time: {perf['average_execution_time']}s")
        print(f"    Total Executions: {perf['total_executions']}")
    
    print(f"\nTotal Errors: {summary['total_errors']}")
    
    print("=" * 80 + "\n")

def clear_observability_data() -> None:
    
    global ACTIVITY_LOG, METRICS
    
    ACTIVITY_LOG.clear()
    METRICS = {
        'total_requests': 0,
        'successful_requests': 0,
        'failed_requests': 0,
        'agent_execution_times': {},
        'tool_usage_count': {},
        'errors': []
    }
    
    logger = logging.getLogger('Observability')
    logger.info("Cleared all observability data")