<template>
  <div>
    <h1>Deepfake Detector</h1>
    <UploadForm @result="goToResult" />
  </div>
</template>

<script>
import UploadForm from "../components/UploadForm.vue";

export default {
  components: { UploadForm },
  methods: {
    goToResult(res) {
      this.$router.push({ name: "Result", state: { result: res } });
    },
  },
};
</script>
