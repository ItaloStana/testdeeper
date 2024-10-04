<template>
  <div>
    <h1>Usuários</h1>
    <button @click="showModal = true">Adicionar Usuário</button>
    <table>
      <thead>
        <tr>
          <th>Username</th>
          <th>Roles</th>
          <th>Timezone</th>
          <th>Is Active?</th>
          <th>Last Update At</th>
          <th>Create At</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user._id">
          <td>{{ user.username }}</td>
          <td>{{ user.roles.join(", ") }}</td>
          <td>{{ user.preferences.timezone }}</td>
          <td>{{ user.active }}</td>
          <td>{{ formatDate(user.updated_at) }}</td>
          <td>{{ formatDate(user.created_at) }}</td>
          <td>
            <button @click="editUser(user)">Editar</button>
            <button @click="deleteUser(user._id)">Deletar</button>
          </td>
        </tr>
      </tbody>
    </table>

    <AppModal v-if="showModal" @close="showModal = false">
      <template #header>
        <h2>{{ isEdit ? "Editar Usuário" : "Adicionar Usuário" }}</h2>
      </template>
      <template #body>
        <form @submit.prevent="isEdit ? updateUser() : createUser()">
          <input v-model="user.username" placeholder="Username" required />
          <input v-model="user.password" placeholder="Password" required />
          <input
            v-model="user.preferences.timezone"
            placeholder="Timezone"
            required
          />
          <button type="submit">
            {{ isEdit ? "Atualizar" : "Adicionar" }}
          </button>
        </form>
      </template>
    </AppModal>
  </div>
</template>

<script>
import AppModal from "./AppModal.vue";

export default {
  components: {
    AppModal,
  },
  data() {
    return {
      users: [],
      showModal: false,
      isEdit: false,
      user: {
        username: "",
        password: "",
        preferences: { timezone: "" },
      },
    };
  },
  methods: {
    fetchUsers() {
      fetch("http://localhost:8081/users")
        .then((response) => response.json())
        .then((data) => {
          this.users = data;
        });
    },
    createUser() {
      fetch("http://localhost:8081/users", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.user),
      }).then(() => {
        this.fetchUsers();
        this.showModal = false;
        this.user = { username: '', password: '', preferences: { timezone: '' } };
      });
    },
    editUser(user) {
      this.user = { ...user };
      this.isEdit = true;
      this.showModal = true;
    },
    updateUser() {
      fetch(`http://localhost:8081/users/${this.user._id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.user),
      }).then(() => {
        this.fetchUsers();
        this.showModal = false;
        this.user = { username: '', password: '', preferences: { timezone: '' } };
        this.isEdit = false;
      });
    },
    deleteUser(userId) {
      if (confirm("Tem certeza que deseja deletar este usuário?")) {
        fetch(`http://localhost:8081/users/${userId}`, {
          method: "DELETE",
        }).then(() => {
          this.fetchUsers();
        });
      }
    },
    formatDate(dateString) {
      const options = {year: 'numeric', month:'2-digit', day:'2-digit', hour:'2-digit', minute:'2-digit' };
      return new Date(dateString).toLocaleDateString("pt-BR", options);
    },
  },
  mounted() {
    this.fetchUsers();
  },
};
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 8px;
  text-align: left;
  border: 1px solid #ddd;
}

th {
  background-color: #f2f2f2;
}

button {
  margin-right: 5px;
}
</style>
