pub mod v1;

use serde::{Deserialize, Serialize};
use std::str::FromStr;

use v1::PayloadV1;

#[derive(Serialize, Deserialize)]
#[serde(untagged)]
pub enum Payloads {
    V1(PayloadV1),
}

impl FromStr for Payloads {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let parts: Vec<&str> = s.split('$').collect();

        match parts.first() {
            Some(&"v1") => {
                // "v1", "{policy}", "{nonce}", "{ciphertext}"
                if parts.len() != 4 {
                    return Err("V1 payload must have exactly 4 parts".to_string());
                }

                let p: u8 = parts[1]
                    .parse::<u8>()
                    .map_err(|_| "V1 payload policy must be u8")?;

                Ok(Payloads::V1(PayloadV1 {
                    p,
                    n: parts[2].to_string(),
                    ct: parts[3].to_string(),
                }))
            }
            _ => Err("Invalid payload of unmatched type/version".to_string()),
        }
    }
}
