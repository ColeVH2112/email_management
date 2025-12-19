from agents import gatekeeper, analyst, secretary

def morning_briefing():
    print("Starting Morning Council...\n")

    daily_report = "# Daily Briefing \n\n"

    for email in inbox:
        #Gatekeeper
        decision = gatekeeper.run(email['body'])

        if decision.get("action") == "DELETE":
            print (f"Deleting email from {email['sender']}")
            continue

        #Analyst
        data = analyst.run(email['body'])

        #Secretary
        summary = secretary.run(email['body'], data)

        #Add to report
        daily_report += f"- *{email['sender']}* : {summary['text']}\n"

        if data.get("has_event"):
            daily_report += f" **EVENT:** {data['event_name']} @ {data['data']} ({data['location']})\n"
        daily_report += "---\n"

    print("\n" + daily_report)

if __name__ = "__main__":
    morning_briefing()

    
