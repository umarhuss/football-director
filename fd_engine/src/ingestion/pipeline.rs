use std::{error::Error, path::Path};
use crate::ingestion::event::Event;


pub fn parse_events(data: &Path) -> Result<Vec<Event>, Box<dyn Error>>{
    let contents = std::fs::read_to_string(data)?;
    let events: Vec<Event> = serde_json::from_str(&contents)?;
    Ok(events)
}

