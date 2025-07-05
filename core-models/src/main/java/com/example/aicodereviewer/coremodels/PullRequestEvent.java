package com.example.aicodereviewer.coremodels;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PullRequestEvent {

    @NotBlank(message = "Event action cannot be blank")
    private String action; // e.g., "opened", "synchronize", "reopened"

    @NotNull(message = "Pull request details cannot be null")
    private PullRequestDetails pullRequest;

    @NotNull(message = "Repository details cannot be null")
    private RepositoryDetails repository;

    // Inner class for Pull Request details
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class PullRequestDetails {
        @NotNull(message = "Pull request number cannot be null")
        private Long number; // PR number

        @NotBlank(message = "Pull request title cannot be blank")
        private String title;

        @NotBlank(message = "Head SHA cannot be blank")
        private String headSha; // SHA of the head commit of the PR branch

        @NotBlank(message = "Base SHA cannot be blank")
        private String baseSha; // SHA of the base commit (target branch)

        @NotBlank(message = "Pull request HTML URL cannot be blank")
        private String htmlUrl; // URL to the PR on GitHub

        @NotBlank(message = "User login cannot be blank")
        private String userLogin; // User who created/updated the PR
    }

    // Inner class for Repository details
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class RepositoryDetails {
        @NotBlank(message = "Repository name cannot be blank")
        private String name; // e.g., "my-awesome-repo"

        @NotBlank(message = "Repository full name cannot be blank")
        private String fullName; // e.g., "username/my-awesome-repo"

        @NotBlank(message = "Repository HTML URL cannot be blank")
        private String htmlUrl; // URL to the repository

        @NotBlank(message = "Repository clone URL cannot be blank")
        private String cloneUrl; // URL to clone the repository
    }

    // We can add more fields as needed, like sender information, installation ID for GitHub Apps, etc.
    // For example:
    // private String senderLogin;
    // private Long installationId;
}
