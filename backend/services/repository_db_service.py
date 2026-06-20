from database.mongo_db import get_collection


# =========================
# SAVE REPOSITORY ANALYSIS
# =========================

async def save_repository_analysis(data):

    collection = get_collection(
        "repositories"
    )

    await collection.insert_one(
        data
    )


# =========================
# GET REPOSITORY BY URL
# =========================

async def get_repository_by_url(
    repo_url
):

    collection = get_collection(
        "repositories"
    )

    return await collection.find_one(
        {
            "repo_url": repo_url
        }
    )


# =========================
# DELETE REPOSITORY BY URL
# =========================

async def delete_repository_by_url(
    repo_url
):

    collection = get_collection(
        "repositories"
    )

    result = await collection.delete_many(
        {
            "repo_url": repo_url
        }
    )

    print(
        f"DELETED REPOSITORIES = "
        f"{result.deleted_count}"
    )

    return result.deleted_count


# =========================
# FORCE REANALYZE
# =========================

async def force_reanalyze_repository(
    repo_url
):

    deleted_count = (
        await delete_repository_by_url(
            repo_url
        )
    )

    print(
        f"FORCE REANALYZE -> "
        f"REMOVED {deleted_count} "
        f"OLD RECORDS"
    )

    return True


# =========================
# CHECK EXISTENCE
# =========================

async def repository_exists(
    repo_url
):

    collection = get_collection(
        "repositories"
    )

    count = await collection.count_documents(
        {
            "repo_url": repo_url
        }
    )

    return count > 0