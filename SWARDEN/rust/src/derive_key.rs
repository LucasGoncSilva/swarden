use argon2::{Algorithm::Argon2id, Argon2, Params, Version::V0x13};
use cached::{SizedCache, proc_macro::cached};

static KIBIBYTE: u32 = 1; // Argon2id recieves memory_cost as KiB
static MEBIBYTE: u32 = 1024 * KIBIBYTE;
static GIBIBYTE: u32 = 1024 * MEBIBYTE;

pub struct CryptoPolicy {
    pub tc: u32, // Time Cost
    pub mc: u32, // Memory Cost
    pub p: u32,  // Parallelism
    pub l: u8,   // Length
}

pub fn get_policy(v: u8) -> CryptoPolicy {
    match v {
        1 => CryptoPolicy {
            tc: 4,
            mc: 4 * GIBIBYTE,
            p: 1,
            l: 32,
        },
        2 => CryptoPolicy {
            tc: 5,
            mc: 3 * GIBIBYTE,
            p: 8,
            l: 32,
        },
        3 => CryptoPolicy {
            tc: 260,
            mc: 64 * MEBIBYTE,
            p: 1,
            l: 32,
        },
        4 => CryptoPolicy {
            tc: 128,
            mc: 128 * MEBIBYTE,
            p: 8,
            l: 32,
        },
        0 => CryptoPolicy {
            tc: 6,
            mc: 131072,
            p: 1,
            l: 32,
        },
        _ => panic!("Unknown version for policy"),
    }
}

#[cached(
    ty = "SizedCache<String, [u8; 32]>",
    create = "{ SizedCache::with_size(4) }",
    convert = r#"{ format!("{}{}{}", master_key, system_pepper, policy_version) }"#
)]
pub fn _derive_key(master_key: &str, system_pepper: &str, policy_version: u8) -> [u8; 32] {
    let policy: CryptoPolicy = get_policy(policy_version);

    let params: Params =
        Params::new(policy.mc, policy.tc, policy.p, Some(policy.l.into())).unwrap();

    let argon2: Argon2<'_> = Argon2::new(Argon2id, V0x13, params);

    let mut output: [u8; 32] = [0u8; 32];

    argon2
        .hash_password_into(master_key.as_bytes(), system_pepper.as_bytes(), &mut output)
        .unwrap();

    output
}
