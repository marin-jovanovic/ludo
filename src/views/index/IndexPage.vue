<template>
  <BaseUserTemplate>
    <div class="container mt-2">
      <div class="row">
        <BasePortfolioList
          @selectUpdate="updateSelectedList"
          @increase-by="updateSelectedForChart"
          :selectedForChart="selected"
        ></BasePortfolioList>
      </div>
    </div>

    <BaseMessage ref="message"></BaseMessage>
  </BaseUserTemplate>
</template>

<script>
import { useToast } from "vue-toastification";
import BaseUserTemplate from "@/components/BaseUserTemplate.vue";
import BaseMessage from "@/components/BaseMessage.vue";
import BasePortfolioList from "@/components/BasePortfolioList.vue";

export default {
  setup() {
    const toast = useToast();
    // toast("notif test");
    return { toast };
  },

  mounted() {
    // this.toast("hello again");
    // console.log("mounted");
    // console.log("mounted", this.selected);
    // this.$refs.message.showMessage(true, "hello", "world");
  },
  data() {
    return {
      selected: {},
      selectedList: {},
    };
  },
  methods: {
    updateSelectedList(pl) {
      console.log("checkobx tick", pl);
      console.log("base");

      let o = {
        portfolio: pl.portfolio,
        section: pl.locationPayload.oldSection,
        type: pl.locationPayload.oldType,
      };
      console.table(o);

      let isSelected = pl.locationPayload.isSelected;
      console.log(isSelected);

      if (!(o.portfolio in this.selectedList)) {
        console.log("new portfolio");
        this.selectedList[o.portfolio] = new Set();
      }

      if (isSelected) {
        this.selectedList[o.portfolio].add({
          section: o.section,
          type: o.type,
        });
      } else {
        this.selectedList[o.portfolio].delete({
          section: o.section,
          type: o.type,
        });
      }

      for (const [key, value] of Object.entries(this.selectedList)) {
        console.log(key);
        console.table(value);
      }
    },
    showSelected() {
      console.log(this.selected);
    },
  },
  components: { BaseUserTemplate, BaseMessage, BasePortfolioList },
};
</script>
