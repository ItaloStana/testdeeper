<template>
    <div class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <slot name="header"></slot>
          <button class="close" @click="$emit('close')">X</button>
        </div>
        <div class="modal-body">
          <slot name="body"></slot>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AppModal',
  };
  </script>
  
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .modal {
    background-color: white;
    border-radius: 8px;
    padding: 20px;
    width: 300px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
  
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .close {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
  }
  
  .modal-body {
    margin-top: 10px;
  }
  </style>
  