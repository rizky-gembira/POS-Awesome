<template>
  <v-app class="container1">
    <v-main>
      <!-- 🔝 Navbar -->
      <Navbar @changePage="setPage($event)"></Navbar>

      <!-- 📄 Dynamic Page -->
      <component v-bind:is="page" class="mx-4 md-4"></component>

      <!-- 🔔 Marketing Program Popup -->
      <v-dialog v-model="showProgram" max-width="600">
        <v-card v-if="programs.length > 0">
          <v-card-title class="headline">
            📢 {{ programs[currentIndex].nama_program }}
          </v-card-title>
          <v-card-text>
            <p>
              <b>Berlaku:</b>
              {{ programs[currentIndex].berlaku_dari }}
              s/d
              {{ programs[currentIndex].berlaku_sampai }}
            </p>
            <div
              class="program-details"
              v-html="programs[currentIndex].details"
            ></div>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text v-if="currentIndex > 0" @click="prevProgram">
              ⬅️ Sebelumnya
            </v-btn>
            <v-btn
              text
              v-if="currentIndex < programs.length - 1"
              @click="nextProgram"
            >
              Berikutnya ➡️
            </v-btn>
            <v-btn
              color="primary"
              text
              v-if="currentIndex === programs.length - 1"
              @click="showProgram = false"
            >
              OK, Mengerti
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-main>
  </v-app>
</template>

<script>
import Navbar from "./components/Navbar.vue";
import POS from "./components/pos/Pos.vue";
import Payments from "./components/payments/Pay.vue";

export default {
  data() {
    return {
      page: "POS",
      programs: [],
      currentIndex: 0,
      showProgram: false,
    };
  },
  components: {
    Navbar,
    POS,
    Payments,
  },
  methods: {
    setPage(page) {
      this.page = page;
    },
    remove_frappe_nav() {
      this.$nextTick(function () {
        $(".page-head").remove();
        $(".navbar.navbar-default.navbar-fixed-top").remove();
      });
    },
    prevProgram() {
      if (this.currentIndex > 0) this.currentIndex--;
    },
    nextProgram() {
      if (this.currentIndex < this.programs.length - 1) this.currentIndex++;
    },
    fetchMarketingProgram() {
      frappe.call({
        method: "posawesome.posawesome.api.marketing_program.get_active_marketing_program",
        args: {},
        callback: (r) => {
          if (r.message && r.message.length > 0) {
            this.programs = r.message;
            this.currentIndex = 0;
            this.showProgram = true;
          }
        },
      });
    },
  },
  mounted() {
    this.remove_frappe_nav();
    this.fetchMarketingProgram();
  },
  created() {
    setTimeout(() => {
      this.remove_frappe_nav();
    }, 1000);
  },
};
</script>

<style scoped>
.container1 {
  margin-top: 0px;
}

/* pastikan text di popup terbaca jelas */
.program-details {
  color: #000 !important;
  opacity: 1 !important;
  font-size: 14px;
  line-height: 1.4;
}
</style>
