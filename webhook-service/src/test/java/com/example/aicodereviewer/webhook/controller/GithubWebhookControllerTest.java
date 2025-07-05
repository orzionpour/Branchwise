package com.example.aicodereviewer.webhook.controller;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.reactive.WebFluxTest;
import org.springframework.context.ApplicationContext;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.web.reactive.server.WebTestClient;

@ExtendWith(SpringExtension.class)
@WebFluxTest(controllers = GithubWebhookController.class)
class GithubWebhookControllerTest {

    private static final Logger logger = LoggerFactory.getLogger(GithubWebhookControllerTest.class);

    @Autowired
    private WebTestClient webTestClient;

    @Autowired
    private ApplicationContext context;

    @BeforeEach
    void setUp() {
        // You can check if the controller is loaded
        // GithubWebhookController controller = context.getBean(GithubWebhookController.class);
        // assertNotNull(controller);
        logger.info("GithubWebhookControllerTest setup complete. WebTestClient initialized.");
    }

    @Test
    void handlePingEvent() {
        webTestClient.post().uri("/api/v1/webhooks/github/events")
                .contentType(MediaType.APPLICATION_JSON)
                .header("X-GitHub-Event", "ping")
                .header("X-GitHub-Delivery", "test-delivery-id-ping")
                .bodyValue("{ \"zen\": \"Keep it simple\" }")
                .exchange()
                .expectStatus().isOk()
                .expectBody(String.class).isEqualTo("Pong! Ping event received successfully.");
        logger.info("Test handlePingEvent completed successfully.");
    }

    @Test
    void handlePullRequestEvent_Opened() {
        String prPayload = """
                {
                  "action": "opened",
                  "number": 1,
                  "pull_request": {
                    "html_url": "https://github.com/testuser/test-repo/pull/1",
                    "head": { "sha": "test-head-sha" },
                    "base": { "sha": "test-base-sha" }
                  },
                  "repository": {
                    "name": "test-repo",
                    "full_name": "testuser/test-repo",
                    "clone_url": "https://github.com/testuser/test-repo.git"
                  }
                }""";

        webTestClient.post().uri("/api/v1/webhooks/github/events")
                .contentType(MediaType.APPLICATION_JSON)
                .header("X-GitHub-Event", "pull_request")
                .header("X-GitHub-Delivery", "test-delivery-id-pr")
                .bodyValue(prPayload)
                .exchange()
                .expectStatus().isOk()
                .expectBody(String.class).isEqualTo("Event received successfully.");
        logger.info("Test handlePullRequestEvent_Opened completed successfully.");
    }

    @Test
    void handleUnknownEvent() {
        webTestClient.post().uri("/api/v1/webhooks/github/events")
                .contentType(MediaType.APPLICATION_JSON)
                .header("X-GitHub-Event", "issues") // An event type not explicitly handled yet
                .header("X-GitHub-Delivery", "test-delivery-id-unknown")
                .bodyValue("{ \"issue\": { \"title\": \"New Issue\" } }")
                .exchange()
                .expectStatus().isAccepted() // As per current controller logic
                .expectBody(String.class).isEqualTo("Event received but not specifically processed.");
        logger.info("Test handleUnknownEvent completed successfully.");
    }

    @Test
    void handleEvent_missingGithubEventHeader() {
        webTestClient.post().uri("/api/v1/webhooks/github/events")
                .contentType(MediaType.APPLICATION_JSON)
                .header("X-GitHub-Delivery", "test-delivery-id-missing-header")
                .bodyValue("{ \"data\": \"some data\" }")
                .exchange()
                .expectStatus().isBadRequest(); // Spring typically returns 400 for missing required headers
        logger.info("Test handleEvent_missingGithubEventHeader completed successfully.");
    }
}
