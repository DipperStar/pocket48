<template>
  <div class="col-md-8 container-fluid" id="logo">
    <div class="row">
      <div class="col-md-12">
        <div class="row" id="headfirst">
          <div class="col-7">
            <h1 style="padding: 10px 0px 10px 40px;">
              <b-img v-bind="userProps" rounded alt="口袋房间" :src=icon></b-img>
            </h1>
          </div>
          <div v-if=loginstatus class="col" align="right" style="padding: 20px 20px 0px 0px;">
            <b-img v-bind="userProps" rounded="circle" alt="头像" :src=user.avatar></b-img>
            <b-button @click="onremovetoken" variant="primary">{{ user.nickname }}</b-button>
          </div>
          <div v-else class="col" align="right" style="padding: 20px 20px 0px 0px;">
            <b-button variant="danger" v-b-modal.login-modal>登录</b-button>
          </div>
        </div>
        <hr>
        <alert v-bind:message="message" v-if="showMessage"></alert>
        <table class="table table-hover">
          <thead>
          <tr>
            <th scope="col">房间</th>
            <th scope="col">成员</th>
            <th scope="col">操作</th>
          </tr>
          </thead>
          <tbody is="transition-group" name="fade">
          <tr v-for="(todo, index) in member" :key="index">
            <td style="text-align: center" :style="{backgroundColor:todo.color}">
              {{ todo.roomName }}
            </td>
            <td style="text-align: center" :style="{backgroundColor:todo.color}">
              <b-img v-bind="teamProps" alt="队伍" :src=todo.icon></b-img>
              {{ todo.ownerName }}
            </td>
            <td style="text-align: center" :style="{backgroundColor:todo.color}">
              <b-button variant="outline-danger"
                        size="sm"
                        @click="onremoveMember(todo)">
                取关
              </b-button>
            </td>
          </tr>
          </tbody>
        </table>
        <div align="middle">
          <b-button variant="outline-primary" size="sm" v-b-modal.addmember-modal>+</b-button>
        </div>
        <hr>
        <table class="table">
          <thead>
          <tr class="row">
            <th class="col-2">时间</th>
            <th class="col-3">成员</th>
            <th class="col-7">消息</th>
          </tr>
          </thead>
          <tbody is="transition-group" name="fade">
          <tr class="row" v-for="(todo, index) in chat" :key="index">
            <td class="col-2" style="text-align:center;vertical-align:middle;"
                :style="{backgroundColor:todo.color}">
              {{ todo.time }}
            </td>
            <td class="col-3" style="text-align:center;vertical-align:middle;"
                :style="{backgroundColor:todo.color}">
              <b-img v-bind="avaterProps" rounded="circle" alt="头像" :src=todo.avatar></b-img>
              <br>
              {{ todo.name }}
            </td>
            <td class="col-7" style="vertical-align:middle;" :style="{backgroundColor:todo.color}">
              <b-button v-if="msgtype(todo)" variant="link"
                        v-b-modal.picture-modal @click="frepicture(todo.mesg)">
                <b-img-lazy alt="消息图片" :src=todo.mesg width="90" height="90"></b-img-lazy>
              </b-button>
              <div v-else v-html="todo.mesg">{{ todo.mesg }}</div>
            </td>
          </tr>
          </tbody>
        </table>
        <hr>
      </div>
    </div>
    <b-modal ref="picture"
             id="picture-modal"
             title="图片"
             body-bg-variant="light"
             size="lg"
             centered
             hide-header
             hide-footer>
      <template>
        <b-img alt="消息图片" :src=nowpic style="width:100%"></b-img>
      </template>
    </b-modal>
    <b-modal ref="login"
             id="login-modal"
             title="登录"
             hide-footer>
      <b-form @submit="onLogin" @reset="onReset" class="w-100">
        <b-form-group id="form-phone-group"
                      label="手机号:"
                      label-for="form-phone-input">
          <b-form-input id="form-phone-input"
                        type="text"
                        v-model="loginForm.phone"
                        required
                        placeholder="">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-password-group"
                      label="密码"
                      label-for="form-password-input">
          <b-form-input id="form-password-input"
                        type="text"
                        v-model="loginForm.password"
                        required
                        placeholder="">
          </b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">登录</b-button>
        <b-button type="reset" variant="danger">清空</b-button>
      </b-form>
    </b-modal>

    <b-modal ref="addmember"
             id="addmember-modal"
             title="添加成员"
             hide-footer>
      <b-form @submit="onAddMember" class="w-100">
        <b-form-group id="form-member-group"
                      label="成员姓名:"
                      label-for="form-member-input">
          <b-form-input id="form-member-input"
                        type="text"
                        v-model="addmemberform.name"
                        required
                        placeholder="">
          </b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">添加</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
  import axios from 'axios';
  import Alert from './Alert';

  export default {
    data: function () {
      return {
        timer: 0,
        token: this.$cookie.get('token'),
        message: '',
        nowpic: '',
        showMessage: false,
        loginstatus: false,
        member: [],
        chat: [],
        icon: 'static/48.png',
        userProps: {width: 60, height: 60, class: 'm1'},
        avaterProps: {width: 45, height: 45, class: 'm1'},
        teamProps: {width: 40, height: 20, class: 'm1'},
        user: {
          avatar: '',
          nickname: '',
        },
        loginForm: {
          phone: '',
          password: '',
        },
        addmemberform: {
          name: '',
        },
      };
    },
    components: {
      alert: Alert,
    },
    methods: {
      // eslint-disable-next-line consistent-return
      msgtype(todo) {
        if (todo.type === 'IMAGE') {
          return true;
        }
      },
      frepicture(picture) {
        this.nowpic = picture;
      },
      init() {
        const path = 'http://144.48.142.227:5000/cheak';
        const payload = {
          token: this.token,
        };
        axios.post(path, payload)
          .then((res) => {
            if (!res.data.status) {
              this.message = '请登录！';
              this.showMessage = true;
            } else {
              this.user.avatar = res.data.avatar;
              this.user.nickname = res.data.nickname;
              this.loginstatus = true;
              this.member = res.data.member;
              this.token = res.data.token;
              this.getChat();
            }
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      },
      getChat() {
        const path = 'http://144.48.142.227:5000/chat';
        const payload = {
          token: this.token,
        };
        axios.post(path, payload)
          .then((res) => {
            this.chat = res.data.chat;
            if (this.chat.length === 0) {
              this.message = '没有关注的小偶像，请添加！';
              this.showMessage = true;
            }
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      },
      login(payload) {
        const path = 'http://144.48.142.227:5000/login';
        axios.post(path, payload)
          .then((res) => {
            this.$cookie.set('token', res.data.token, 7);
            this.token = res.data.token;
            this.member = res.data.member;
            this.user.avatar = res.data.avatar;
            this.user.nickname = res.data.nickname;
            this.loginstatus = true;
            this.getChat();
            this.message = `登录成功！token:${this.token}`;
            this.showMessage = true;
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.log(error);
            this.getMembers();
          });
      },
      addMember(payload) {
        const path = 'http://144.48.142.227:5000/addmember';
        axios.post(path, payload)
          .then((res) => {
            this.member = res.data.member;
            this.getChat();
            this.initForm();
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      },
      // 删除数据
      removeMember(member) {
        const path = 'http://144.48.142.227:5000/removemember';
        axios.post(path, member)
          .then((res) => {
            this.member = res.data.member;
            this.getChat();
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      },
      onremoveMember(todo) {
        // eslint-disable-next-line
        const payload = {
          roomId: todo.roomId,
          token: this.token,
        };
        this.removeMember(payload);
      },
      // 重置数据
      initForm() {
        this.loginForm.phone = '';
        this.loginForm.password = '';
        this.loginForm.member = '';
        this.addmemberform.name = '';
      },
      onLogin(evt) {
        evt.preventDefault();
        this.$refs.login.hide();
        const payload = {
          phone: this.loginForm.phone,
          password: this.loginForm.password,
        };
        this.login(payload);
        this.initForm();
      },
      // 增加成员
      onAddMember(evt) {
        evt.preventDefault();
        this.$refs.addmember.hide();
        const payload = {
          name: this.addmemberform.name,
          token: this.token,
        };
        this.addMember(payload);
      },
      onReset(evt) {
        evt.preventDefault();
        // this.$refs.addBookModal.hide();
        this.initForm();
      },
      onremovetoken(evt) {
        evt.preventDefault();
        this.$cookie.delete('token');
        const path = 'http://144.48.142.227:5000/removetoken';
        const payload = {
          token: this.token,
        };
        axios.post(path, payload)
          .then(() => {
            this.loginstatus = false;
            this.init();
          });
      },
    },

    created() {
      // 定时刷新数据
      this.init();
      if (this.timer) {
        clearInterval(this.timer);
      } else {
        this.timer = setInterval(() => {
          this.getChat();
        }, 60000);
      }
    },
    destroyed() {
      clearInterval(this.timer);
    },
  };
</script>

<style scoped>
  th {
    text-align: center
  }

  .fade-enter-active, .fade-leave-active {
    transition: opacity 1s;
  }

  .fade-enter, .fade-leave-to {
    opacity: 0;
  }

  #logo {
    margin-top: 20px;
    background: #f8f8f8;
    color: #000;
    background-size: 100% 100%;
    height: 100%;
    /*position: fixed;*/
    width: 100%
  }

  #headfirst {
    background: url("../../static/headfirst1.png");
    background-repeat: repeat-x;
    /*background-size: 100% 100%;*/
    /*height: 100%;*/
    /*position: fixed;*/
    /*width: 100%*/
  }
</style>
