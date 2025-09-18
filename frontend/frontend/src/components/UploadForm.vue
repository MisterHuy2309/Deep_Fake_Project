<template>
  <div class="upload-form">
    <h2>Deepfake Detection</h2>

    <div class="upload-section">
      <!-- Khung upload ảnh -->
      <div class="upload-box">
        <h3>Ảnh</h3>

        <!-- Nút upload ảnh -->
        <input
          type="file"
          accept="image/*"
          ref="imageInput"
          style="display: none"
          @change="handleImageUpload"
        />
        <button class="btn-primary" @click="$refs.imageInput.click()">
          Upload image
        </button>

        <!-- Preview -->
        <div v-if="previewImage" class="preview">
          <img :src="previewImage" alt="Preview" />
        </div>
      </div>

      <!-- Khung upload video/link -->
      <div class="upload-box">
        <h3>Video</h3>
        <label>Nhập link:</label>
        <input
          class="input-text"
          type="text"
          v-model="videoLink"
          @input="resetImage"
          placeholder="https://..."
        />

        <label>Hoặc upload:</label>
        <input type="file" accept="video/*" @change="handleVideoUpload" />
      </div>
    </div>

    <button class="btn-submit" @click="submitForm">Kiểm tra</button>

    <!-- Kết quả -->
    <div v-if="result" class="result">
      <p>Kết quả: <strong>{{ result }}</strong></p>
      <p>Score: <strong>{{ score }}</strong></p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "UploadForm",
  data() {
    return {
      selectedFile: null,
      videoLink: "",
      previewImage: null,
      result: null,
      score: null,
    };
  },
  methods: {
    handleImageUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.selectedFile = file;
        this.previewImage = URL.createObjectURL(file);

        // Reset video link nếu có
        this.videoLink = "";
      }
    },
    handleVideoUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.selectedFile = file;
        this.previewImage = null; // reset preview nếu là video
      }
    },
    resetImage() {
      // Nếu nhập link thì xóa ảnh
      if (this.videoLink) {
        this.selectedFile = null;
        this.previewImage = null;
      }
    },
    async submitForm() {
      try {
        let formData = new FormData();

        if (this.videoLink) {
          formData.append("url", this.videoLink);
          this.selectedFile = null;
          this.previewImage = null;
        } else if (this.selectedFile) {
          formData.append("file", this.selectedFile);
        } else {
          alert("Vui lòng chọn ảnh, video hoặc nhập link!");
          return;
        }

        const response = await axios.post(
          "http://127.0.0.1:8000/predict_video",
          formData,
          { headers: { "Content-Type": "multipart/form-data" } }
        );

        this.result = response.data.result;
        this.score = response.data.score;
      } catch (error) {
        console.error("Upload thất bại:", error);
        alert("Có lỗi khi upload!");
      }
    },
  },
};
</script>

<style scoped>
.upload-form {
  display: flex;
  flex-direction: column;
  gap: 25px;
  align-items: center;
}

.upload-form h2 {
  color: #6c5ce7;
  font-size: 26px;
  font-weight: bold;
}

.upload-section {
  display: flex;
  justify-content: center;
  gap: 30px;
  width: 100%;
  max-width: 950px;
}

.upload-box {
  flex: 1;
  padding: 20px;
  border: 1px solid #e0dff7;
  border-radius: 12px;
  box-shadow: 0 3px 8px rgba(108, 92, 231, 0.15);
  background: #faf9ff;
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: center;
}

.upload-box h3 {
  margin-bottom: 5px;
  color: #6c5ce7;
}

.input-text {
  width: 100%;
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid #dcdcdc;
  outline: none;
}

.input-text:focus {
  border-color: #6c5ce7;
  box-shadow: 0 0 5px rgba(108, 92, 231, 0.3);
}

.preview img {
  max-width: 100%;
  max-height: 200px;
  object-fit: contain;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-top: 10px;
}

.btn-primary {
  background: #6c5ce7;
  color: white;
  border: none;
  padding: 10px 18px;
  cursor: pointer;
  border-radius: 8px;
  transition: 0.3s;
  font-weight: bold;
}
.btn-primary:hover {
  background: #5a4bce;
}

.btn-submit {
  background: linear-gradient(135deg, #6c5ce7, #8e7efc);
  color: white;
  border: none;
  padding: 12px 25px;
  cursor: pointer;
  border-radius: 10px;
  font-size: 16px;
  transition: 0.3s;
  font-weight: bold;
}
.btn-submit:hover {
  background: linear-gradient(135deg, #5a4bce, #7d6cf9);
}

.result {
  margin-top: 15px;
  font-size: 18px;
  background: #f3f1fe;
  padding: 12px 18px;
  border-radius: 8px;
  border: 1px solid #ddd;
}
</style>
