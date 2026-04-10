import NextAuth, { type NextAuthOptions } from "next-auth";
import GoogleProvider from "next-auth/providers/google";

export const authOptions: NextAuthOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.AUTH_GOOGLE_ID!,
      clientSecret: process.env.AUTH_GOOGLE_SECRET!,
    }),
  ],
  secret: process.env.NEXTAUTH_SECRET,

  callbacks: {
    async jwt({ token, account, profile }) {
      if (account) {
        token.googleId = account.providerAccountId;
      }

      if (profile && "email_verified" in profile) {
        token.emailVerified = Boolean(profile.email_verified);
      }

      return token;
    },

    async session({ session, token }) {
      if (session.user) {
        session.user.googleId = token.googleId as string;
        session.user.emailVerified = token.emailVerified as boolean;
      }

      return session;
    },
  },
};

const handler = NextAuth(authOptions);

export { handler as GET, handler as POST };