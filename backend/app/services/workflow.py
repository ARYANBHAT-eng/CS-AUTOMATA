from typing import Dict, List


def generate_workflow_actions(score: Dict) -> List[Dict]:
    actions = []
    churn_risk = score.get("churn_risk")
    user_segment = score.get("user_segment")

    if churn_risk == "high":
        actions.append(
            {
                "type": "alert",
                "action": "trigger_reengagement_email",
                "priority": "high",
                "reason": "high churn risk due to inactivity",
            }
        )
    elif churn_risk == "medium":
        actions.append(
            {
                "type": "monitor",
                "action": "schedule_followup",
                "priority": "medium",
                "reason": "moderate inactivity detected",
            }
        )

    if user_segment == "power_user":
        actions.append(
            {
                "type": "revenue",
                "action": "trigger_upsell_flow",
                "priority": "high",
                "reason": "high engagement detected, upsell opportunity",
            }
        )

    if not actions:
        actions.append(
            {
                "type": "normal",
                "action": "no_action",
                "priority": "low",
                "reason": "user is stable, no action required",
            }
        )

    priority_order = {"high": 3, "medium": 2, "low": 1}
    actions.sort(key=lambda action: priority_order.get(action["priority"], 0), reverse=True)

    return actions
