<template>
  <div id="app">
    <!-- Header -->
    <header class="header">
      <h1>Deepfake Detection Demo</h1>
    </header>

    <!-- Form upload -->
    <section class="upload-section">
      <UploadForm @upload-finished="handleResult" />
    </section>

    <!-- Bảng kết quả -->
    <section class="result-section" v-if="results.length > 0">
      <ResultTable :results="results" />
    </section>
  </div>
</template>

<script>
import UploadForm from "./components/UploadForm.vue";
import ResultTable from "./components/ResultDisplay.vue";

export default {
  name: "App",
  components: { UploadForm, ResultTable },
  data() {
    return {
      results: [],
    };
  },
  methods: {
    handleResult(data) {
      this.results.push({
        filename: data.filename || this.randomName(),
        fake_score: data.result === "Fake" ? data.score / 100 : 1 - data.score / 100,
        real_score: data.result === "Real" ? data.score / 100 : 1 - data.score / 100,
      });
    },
    randomName() {
      return "upload_" + Math.floor(Math.random() * 10000);
    },
  },
};
</script>

<style>
/* Toàn bộ app */
#app {
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  text-align: center;
  background: linear-gradient(135deg, #6a11cb, #a4508b);
  min-height: 100vh;
  color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Header */
.header {
  width: 100%;
  padding: 20px 0;
  background: rgba(106, 17, 203, 0.9);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}
.header h1 {
  margin: 0;
  font-size: 28px;
  font-weight: bold;
  color: #fff;
}

/* Upload section */
.upload-section {
  margin-top: 30px;
  background: #fff;
  color: #333;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
  width: 90%;
  max-width: 800px;
}

/* Result section */
.result-section {
  margin-top: 40px;
  width: 90%;
  max-width: 900px;
  background: #fff;
  color: #333;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
}
</style>
