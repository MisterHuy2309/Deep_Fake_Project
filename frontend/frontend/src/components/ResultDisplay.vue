<template>
  <div class="result-table" v-if="results && results.length">
    <h2>Kết quả dự đoán</h2>
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th>Tên file</th>
          <th>Fake (%)</th>
          <th>Real (%)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in results" :key="index">
          <td>{{ index + 1 }}</td>
          <td>{{ item.filename || "N/A" }}</td>
          <td>{{ (item.fake_score * 100).toFixed(2) }}</td>
          <td>{{ (item.real_score * 100).toFixed(2) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "ResultTable",
  props: {
    results: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
.result-table {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
table {
  border-collapse: collapse;
  width: 80%;
  text-align: center;
}
th, td {
  border: 1px solid #ddd;
  padding: 8px;
}
th {
  background: #42b883;
  color: white;
}
</style>
