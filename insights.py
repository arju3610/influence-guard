def generate_insight(data):

    score = data['fraud_score']

    if score >= 70:

        return (
            "This creator shows extremely low engagement compared to audience size. "
            "Possible fake audience detected."
        )

    elif score >= 40:

        return (
            "This creator has suspicious engagement patterns. "
            "Further manual review recommended."
        )

    return (
        "This creator demonstrates healthy audience interaction and engagement."
    )


def generate_detailed_insight(fraud_score, engagement, subscribers, videos):
    if fraud_score >= 70:
        insight = (
            f"Critical fraud indicators detected. With {subscribers:,} subscribers and only {engagement}% engagement rate, "
            "this channel shows signs of artificial inflation. The engagement-to-subscriber ratio is abnormally low, "
            "suggesting purchased followers or bot activity."
        )
        recommendation = (
            "Immediate verification required. Cross-check with third-party analytics tools, review recent video comments "
            "for authenticity, and consider audience demographics. Avoid high-value partnerships until confirmed genuine."
        )
    elif fraud_score >= 40:
        insight = (
            f"Moderate risk factors present. {engagement}% engagement rate for {subscribers:,} subscribers raises concerns "
            "about audience quality. While not definitively fake, the metrics don't align with typical organic growth patterns."
        )
        recommendation = (
            "Conduct supplementary analysis. Examine video upload consistency, comment quality, and subscriber growth velocity. "
            "Consider smaller-scale collaborations first to test audience response."
        )
    else:
        insight = (
            f"Strong indicators of authentic engagement. {engagement}% engagement rate with {subscribers:,} subscribers "
            "demonstrates healthy audience interaction. Metrics align with genuine influencer growth patterns."
        )
        recommendation = (
            "Proceed with confidence. This channel shows consistent, organic engagement patterns suitable for brand partnerships. "
            "Monitor performance metrics during collaboration for continued authenticity."
        )

    return insight, recommendation