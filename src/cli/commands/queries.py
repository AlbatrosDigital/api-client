login = """mutation login($password: String!, $username: String!) {
  login(password: $password, username: $username) {
    ... on LoginSuccess {
      __typename
      token {
        accessToken
      }
      user {
        username
      }
    }
    ... on LoginError {
      __typename
      message
    }
  }
}
"""

fueltable = """query fuelTable($id: String!, $draft: String, $speed: Float, $tws: Float, $twa: Float, $waveDir: Float, $sigWaveHeight: Float) {
  digitalShip {
    get(id: $id) {
      name
      fuelTable(draft: $draft, speed: $speed, tws: $tws, twa: $twa, waveDir: $waveDir, sigWaveHeight: $sigWaveHeight)
    }
  }
}
"""