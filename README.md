## Initial input/readme so will update later 

Current plan is just to createa  system that will manage my personal emails for me. Will use API key as well as a locally hosted llm (LLAMA3.2) to go through mailbox then determine which emails contain information that is worth a second look. Then going through and adding events to calendar as well as generating a summary of all the emails for the morning like a normal secretary would. 

Expected to be ran in the morning or whenever was warranted in to have brief of emails.

## Multi Agent System

* **Gatekeeper:** Initially decides if email simply should be deleted or is worht extracting informaiton from
* **Analyst:** Extracts infromation for calendar events (Date, Time, Location)
* **Secretary:** Generates summary for the morning brief.
