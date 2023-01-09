<template>
  <base-user-template> </base-user-template>
</template>
      
    <script>
import BaseUserTemplate from "@/components/BaseUserTemplate.vue";

//   import { apiSettings } from "@/scripts/api/settings";
//   import { userMetaSS } from "@/scripts/session_storage";
export default {
  data() {
    return { username: undefined, profilePhoto: undefined };
  },
  async mounted() {
    //   this.profilePhoto = userMetaSS.getUserMeta()["userProfilePhoto"];
    //   let r = await apiSettings.getSettings();
    //   if (r["auth"]["status"]) {
    //     let pl = r["payload"];
    //     this.username = pl["username"];
    //   }
  },
  components: {
    BaseUserTemplate,
  },
};
</script>
      
    <style>
</style>