#![allow(dead_code)]
use serde::{Deserialize, Serialize};
// Struct to represent the nested fields in the events data
#[derive(Deserialize, Serialize, Debug)]
pub struct NamedEntity {
    pub id: u32,
    pub name: String,
}

#[derive(Deserialize, Serialize, Debug)]
pub struct CarryDetails {
    pub end_location: [f64; 2],
}

#[derive(Deserialize, Serialize, Debug)]
pub struct PassDetails {
    pub length: f64,
    pub angle: f64,
    pub end_location: [f64; 2],
    pub recipient: Option<NamedEntity>,
    pub height: Option<NamedEntity>,
    pub outcome: Option<NamedEntity>,
    pub technique: Option<NamedEntity>,
    pub body_part: Option<NamedEntity>,
    pub cross: Option<bool>,
    pub switch: Option<bool>,
    pub through_ball: Option<bool>,
    pub shot_assist: Option<bool>,
    pub goal_assist: Option<bool>,
}

#[derive(Deserialize, Serialize, Debug)]
pub struct ShotDetails {
    pub statsbomb_xg: f64,
    pub end_location: [f64; 2],
    pub outcome: NamedEntity,
    pub technique: NamedEntity,
    pub body_part: NamedEntity,
    pub first_time: Option<bool>,
    pub one_on_one: Option<bool>,
    pub open_goal: Option<bool>,
}

#[derive(Deserialize, Serialize, Debug)]
pub struct DuelDetails {
    #[serde(rename = "type")]
    pub duel_type: NamedEntity,
    pub outcome: Option<NamedEntity>,
}

#[derive(Deserialize, Serialize, Debug)]
pub struct InterceptionDetails {
    pub outcome: NamedEntity,
}

#[derive(Deserialize, Serialize, Debug)]
pub struct ClearanceDetails {
    pub aerial_won: Option<bool>,
    pub body_part: Option<NamedEntity>,
    pub head: Option<bool>,
}

#[derive(Deserialize, Serialize, Debug)]
pub struct BlockDetails {
    pub deflection: Option<bool>,
    pub offensive: Option<bool>,
    pub save_block: Option<bool>,
}

#[derive(Deserialize, Serialize, Debug)]
pub struct BallRecoveryDetails {
    pub offensive: Option<bool>,
    pub recovery_failure: Option<bool>,
}

#[derive(Deserialize, Serialize, Debug)]
pub struct FoulCommittedDetails {
    pub advantage: Option<bool>,
    pub offensive: Option<bool>,
    pub penalty: Option<bool>,
    #[serde(rename = "type")]
    pub foul_type: Option<NamedEntity>,
    pub card: Option<NamedEntity>,
}

#[derive(Deserialize, Serialize, Debug)]
pub struct FoulWonDetails {
    pub advantage: Option<bool>,
    pub defensive: Option<bool>,
    pub penalty: Option<bool>,
}

#[derive(Deserialize, Serialize, Debug)]
pub struct MiscontrolDetails {
    pub aerial_won: Option<bool>,
}

#[derive(Deserialize, Serialize, Debug)]
pub struct Event {
    pub id: u32,
    pub index: u32,
    pub period: u32,
    pub timestamp: String,
    pub minute: u32,
    pub second: u32,
    #[serde(rename = "type")] // type is a keyword in rust so change this field to the
    pub event_type: NamedEntity, // this one
    pub team: NamedEntity,
    pub duration: f64,

    // Handle field that could be present
    pub player: Option<NamedEntity>,
    pub position: Option<NamedEntity>,
    pub location: Option<[f64; 2]>,
    pub related_events: Option<Vec<String>>,
    pub under_pressure: Option<bool>,
    pub counterpress: Option<bool>,
    pub off_camera: Option<bool>,
    pub out: Option<bool>,

    // Event Specific fields
    pub carry: Option<CarryDetails>,
    pub pass: Option<PassDetails>,
    pub shot: Option<ShotDetails>,
    pub duel: Option<DuelDetails>,
    pub interception: Option<InterceptionDetails>,
    pub clearance: Option<ClearanceDetails>,
    pub block: Option<BlockDetails>,
    pub ball_recovery: Option<BallRecoveryDetails>,
    pub foul_committed: Option<FoulCommittedDetails>,
    pub foul_won: Option<FoulWonDetails>,
    pub miscontrol: Option<MiscontrolDetails>,
}
