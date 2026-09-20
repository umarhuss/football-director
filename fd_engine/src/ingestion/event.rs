use serde::{Deserialize,Serialize};

// Struct to represent the nested fields in the events data
#[derive(Deserialize,Serialize,Debug)]
struct NamedEntity{
    id: u32,
    name: String,
}

#[derive(Deserialize,Serialize,Debug)]
struct CarryDetails{
    end_location:[f64;2],
}

#[derive(Deserialize,Serialize,Debug)]
struct Event {
    event_id: u32,
    index: u32,
    period: u32,
    timestamp: String,
    minute: u32,
    second: u32,
    #[serde(rename = "type")] // type is a keyword in rust so change this field to the
    event_type: NamedEntity, // this one
    team: NamedEntity,
    duration: f64,

    // Handle field that could be present
    player: Option<NamedEntity>,
    position: Option<NamedEntity>,
    location: Option<[f64;2]>,
    related_events:Option<Vec<String>>,
    under_pressure:Option<bool>,
    conuterpress: Option<bool>,
    off_camera: Option<bool>,
    out: Option<bool>,

    // Event Specific fields
    carry:Option<CarryDetails>,




}
