// src/App.jsx
import React, { useState } from 'react';
import './App.css'; // Make sure to import the styles

// Player component to represent each player
const Player = ({ name, score, onIncrease, onDecrease, onDelete }) => {
  const [hover, setHover] = useState(false);

  return (
    <div
      className="player"
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
    >
      {hover && (
        <button onClick={onDelete} className="delete-button">
          X
        </button>
      )}
      <span>{name}</span>
      <div className="score-controls">
        <button onClick={onDecrease}>-</button>
        <span>{score}</span>
        <button onClick={onIncrease}>+</button>
      </div>
    </div>
  );
};

// Scoreboard component to manage the player list and scores
const Scoreboard = () => {
  const [players, setPlayers] = useState([
    { id: 1, name: 'Laura', score: 0 },
    { id: 2, name: 'Dustin', score: 0 },
    { id: 3, name: 'Rachel', score: 0 },
    { id: 4, name: 'Travis', score: 0 },
  ]);

  const handleIncrease = (id) => {
    setPlayers(players.map(player => 
      player.id === id ? { ...player, score: player.score + 1 } : player
    ));
  };

  const handleDecrease = (id) => {
    setPlayers(players.map(player => 
      player.id === id ? { ...player, score: player.score - 1 } : player
    ));
  };

  const handleDelete = (id) => {
    setPlayers(players.filter(player => player.id !== id));
  };

  return (
    <div className="scoreboard">
      <header>
        <h1>SCOREBOARD</h1>
        <p>PLAYERS: {players.length}</p>
      </header>
      <div className="player-list">
        {players.map(player => (
          <Player
            key={player.id}
            name={player.name}
            score={player.score}
            onIncrease={() => handleIncrease(player.id)}
            onDecrease={() => handleDecrease(player.id)}
            onDelete={() => handleDelete(player.id)}
          />
        ))}
      </div>
    </div>
  );
};

export default Scoreboard;
