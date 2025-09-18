<template>
  <div>
    <h2>Kết quả phân tích</h2>
    <ResultDisplay :result="result" />
    <router-link to="/">← Về lại Home</router-link>
  </div>
</template>

<script>
import ResultDisplay from "../components/ResultDisplay.vue";

export default {
  components: { ResultDisplay },
  computed: {
    result() {
      return history.state.result || { message: "Chưa có dữ liệu" };
    },
  },
};
</script>
