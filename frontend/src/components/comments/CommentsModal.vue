<script setup lang="ts">
import { ref, onMounted } from "vue";
import {
  getCommentsByPost,
  createComment,
  deleteComment,
  type Comment,
} from "../../services/commentService";
import { useUserStore } from "../../store/userStore";

const props = defineProps<{
  postId: string;
  show: boolean;
}>();

const emit = defineEmits(["close"]);

const userStore = useUserStore();
const comments = ref<Comment[]>([]);
const newComment = ref("");
const replyTo = ref<string | null>(null);
const replies = ref<Record<string, string>>({});

const fetchComments = async () => {
  comments.value = await getCommentsByPost(props.postId);
};

onMounted(fetchComments);

const handleSubmit = async () => {
  if (!newComment.value.trim()) return;

  const comment = await createComment({
    post: props.postId,
    content: newComment.value.trim(),
  });

  if (comment) {
    comments.value.push(comment);
    newComment.value = "";
  }
};

const handleReply = async (parentId: string) => {
  const replyContent = replies.value[parentId];
  if (!replyContent?.trim()) return;

  const reply = await createComment({
    post: props.postId,
    content: replyContent.trim(),
    parent_comment: parentId,
  });

  if (reply) {
    const parent = comments.value.find((c) => c.id === parentId);
    if (parent) {
      parent.replies = parent.replies || [];
      parent.replies.push(reply);
    }
    replies.value[parentId] = "";
    replyTo.value = null;
  }
};

const handleDelete = async (id: string) => {
  const confirmed = window.confirm("¿Eliminar comentario?");
  if (!confirmed) return;

  const success = await deleteComment(id);
  if (success) {
    comments.value = comments.value.filter((c) => c.id !== id);
    comments.value.forEach((c) => {
      if (c.replies) c.replies = c.replies.filter((r) => r.id !== id);
    });
  }
};
</script>

<template>
  <div
    v-if="show"
    class="fixed inset-0 bg-black/70 flex items-center justify-center z-50"
    @click.self="emit('close')"
    @keyup.esc="emit('close')"
    tabindex="0"
  >
    <div
      class="bg-gray-900 px-6 py-4 rounded-lg shadow-lg w-[90%] max-w-[600px] max-h-[90vh] overflow-y-auto text-white"
    >
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-semibold">💬 Comments</h2>
        <button
          @click="emit('close')"
          class="text-white hover:text-red-400 text-xl"
        >
          x
        </button>
      </div>

      <div class="mb-4">
        <textarea
          v-model="newComment"
          rows="3"
          class="w-full p-2 rounded text-black"
          placeholder="Write a comment..."
        ></textarea>
        <button
          @click="handleSubmit"
          class="mt-2 bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded text-sm"
        >
          Comment
        </button>
      </div>

      <div v-if="comments.length" class="space-y-4">
        <div
          v-for="comment in comments"
          :key="comment.id"
          class="bg-white/10 p-3 rounded"
        >
          <div class="text-sm mb-1">
            <strong>{{ comment.user }}</strong> ·
            <span class="text-white/60">{{
              new Date(comment.created_at).toLocaleString()
            }}</span>
          </div>
          <p class="text-sm">{{ comment.content }}</p>
          <div class="flex gap-2 mt-1 text-xs">
            <button @click="replyTo = comment.id" class="hover:underline">
              Reply
            </button>
            <button
              v-if="userStore.user?.id === comment.user"
              @click="handleDelete(comment.id)"
              class="hover:underline text-red-400"
            >
              Delete
            </button>
          </div>

          <!-- Replies -->
          <div
            v-if="comment.replies?.length"
            class="mt-2 pl-4 border-l border-white/20"
          >
            <div
              v-for="reply in comment.replies"
              :key="reply.id"
              class="bg-white/5 p-2 rounded mt-2"
            >
              <div class="text-xs mb-1">
                <strong>{{ reply.user }}</strong> ·
                <span class="text-white/60">{{
                  new Date(reply.created_at).toLocaleString()
                }}</span>
              </div>
              <p class="text-sm">{{ reply.content }}</p>
              <div class="flex gap-2 mt-1 text-xs">
                <button
                  v-if="userStore.user?.id === reply.user"
                  @click="handleDelete(reply.id)"
                  class="hover:underline text-red-400"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>

          <!-- Reply input -->
          <div v-if="replyTo === comment.id" class="mt-2">
            <textarea
              v-model="replies[comment.id]"
              rows="2"
              class="w-full p-2 rounded text-black"
              placeholder="Write a reply..."
            ></textarea>
            <button
              @click="handleReply(comment.id)"
              class="mt-1 bg-blue-600 hover:bg-blue-700 px-3 py-1 rounded text-sm"
            >
              Reply
            </button>
          </div>
        </div>
      </div>

      <div v-else class="text-center text-white/60 mt-4">No comments yet.</div>
    </div>
  </div>
</template>
